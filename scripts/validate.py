#!/usr/bin/env python3
"""Check every design folder: required files, design.yml fields, file types and
sizes, and that model and photo files are what their extension says.

    python3 scripts/validate.py            # all designs
    python3 scripts/validate.py designs/x  # some

Exits 1 and lists the problems if any design fails.
"""

import re
import struct
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DESIGNS = ROOT / "designs"

SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KINDS = {"mount", "holder", "adapter", "replacement-part", "accessory", "other"}
MODEL_EXT = {".stl", ".3mf", ".step", ".stp"}
PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp"}
DOC_FILES = {"design.yml", "README.md"}
MB = 1024 * 1024
MAX_MODEL = 50 * MB
MAX_PHOTO = 5 * MB
MAX_3MF_UNPACKED = 500 * MB


def model_ok(path: Path) -> str | None:
    """None if the file is a plausible STL / 3MF / STEP, else why not."""
    ext = path.suffix.lower()
    data = path.read_bytes()
    if ext == ".stl":
        if len(data) >= 84:
            (count,) = struct.unpack_from("<I", data, 80)
            if len(data) == 84 + 50 * count:
                return None  # binary STL
        head = data[:1024].lstrip().lower()
        if head.startswith(b"solid") and b"facet" in data[:65536].lower():
            return None  # ASCII STL
        return "not a binary or ASCII STL"
    if ext == ".3mf":
        try:
            with zipfile.ZipFile(path) as z:
                names = {i.filename.lower() for i in z.infolist()}
                if sum(i.file_size for i in z.infolist()) > MAX_3MF_UNPACKED:
                    return "unpacks to more than 500 MB"
                if "3d/3dmodel.model" not in names:
                    return "3MF without 3D/3dmodel.model"
        except zipfile.BadZipFile:
            return "3MF that isn't a zip archive"
        return None
    if ext in {".step", ".stp"}:
        if data[:64].lstrip().startswith(b"ISO-10303-21"):
            return None
        return "not a STEP (ISO-10303-21) file"
    return "unsupported model type"


def photo_ok(path: Path) -> bool:
    head = path.read_bytes()[:12]
    return (
        head.startswith(b"\xff\xd8\xff")
        or head.startswith(b"\x89PNG\r\n\x1a\n")
        or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")
    )


def check_meta(meta: object, errors: list[str]) -> None:
    if not isinstance(meta, dict):
        errors.append("design.yml must be a mapping")
        return
    for key in ("title", "summary", "kind", "version", "creator"):
        if meta.get(key) in (None, ""):
            errors.append(f"design.yml: `{key}` is required")
    if meta.get("kind") not in KINDS | {None, ""}:
        errors.append(f"design.yml: `kind` must be one of {', '.join(sorted(KINDS))}")
    if not isinstance(meta.get("version"), int) or meta.get("version", 0) < 1:
        errors.append("design.yml: `version` must be a whole number from 1")

    fits = meta.get("fits") or {}
    devices = fits.get("devices") or [] if isinstance(fits, dict) else []
    platforms = fits.get("battery_platforms") or [] if isinstance(fits, dict) else []
    if not devices and not platforms:
        errors.append("design.yml: `fits` needs at least one device or battery platform")
    for d in devices:
        if not (isinstance(d, dict) and d.get("brand") and d.get("model")):
            errors.append("design.yml: each device needs `brand` and `model`")
    for p in platforms:
        if not (isinstance(p, dict) and p.get("brand") and p.get("platform")):
            errors.append("design.yml: each battery platform needs `brand` and `platform`")
    if platforms and not str(meta.get("safety") or "").strip():
        errors.append("design.yml: `safety` is required for battery platform designs")


def check_design(folder: Path) -> list[str]:
    errors: list[str] = []
    if not SLUG.match(folder.name):
        errors.append("folder name must be lowercase letters, digits and dashes")
    for name in DOC_FILES:
        if not (folder / name).is_file():
            errors.append(f"missing {name}")

    meta_path = folder / "design.yml"
    if meta_path.is_file():
        try:
            check_meta(yaml.safe_load(meta_path.read_text(encoding="utf-8")), errors)
        except yaml.YAMLError as e:
            errors.append(f"design.yml doesn't parse: {e}")

    models = photos = 0
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        rel = path.relative_to(folder)
        ext = path.suffix.lower()
        size = path.stat().st_size
        if str(rel) in DOC_FILES:
            continue
        if rel.parts[0] == "photos" and len(rel.parts) == 2 and ext in PHOTO_EXT:
            photos += 1
            if size > MAX_PHOTO:
                errors.append(f"{rel}: over 5 MB")
            elif not photo_ok(path):
                errors.append(f"{rel}: not a JPEG, PNG or WebP image")
        elif len(rel.parts) == 1 and ext in MODEL_EXT:
            models += 1
            if size > MAX_MODEL:
                errors.append(f"{rel}: over 50 MB")
            elif why := model_ok(path):
                errors.append(f"{rel}: {why}")
        else:
            errors.append(f"{rel}: not allowed (models go at the top, photos in photos/)")
    if not models:
        errors.append("no model file (.stl, .3mf or .step)")
    if not photos:
        errors.append("no photo in photos/")
    return errors


def main(argv: list[str]) -> int:
    if argv:
        folders = [Path(a).resolve() for a in argv]
    else:
        folders = sorted(p for p in DESIGNS.iterdir() if p.is_dir() and not p.name.startswith("_"))
    failed = False
    for folder in folders:
        errors = check_design(folder)
        if errors:
            failed = True
            print(f"{folder.relative_to(ROOT)}:")
            for e in errors:
                print(f"  - {e}")
    if not failed:
        print(f"{len(folders)} design(s) OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
