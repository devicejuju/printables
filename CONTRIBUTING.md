# Contributing a design

## The rules

1. **You made it.** Only original work by you. No remixes or edits of anyone
   else's design, even a CC0 one, and nothing traced or exported from a
   manufacturer's CAD.
2. **It's CC0.** By contributing you dedicate the design to the public domain
   under [CC0 1.0](LICENSE). This can't be taken back: once merged, anyone may
   copy, change and sell it, and it stays in this repository's history and in
   every fork.
3. **It fits something in the catalog.** `design.yml` names at least one
   device or battery platform on [devicejuju.com](https://devicejuju.com).

## Creator certificate

Every commit must end with a sign-off line (`git commit -s` adds it):

```
Signed-off-by: Your Name <you@example.com>
```

The sign-off means you certify:

> (a) I created this contribution myself, in whole, and it is not based on
> anyone else's design;
>
> (b) I have the right to dedicate it to the public domain, and I do so under
> CC0 1.0 Universal, irrevocably;
>
> (c) I understand the contribution and a record of it, including my name and
> email in the sign-off, are public and kept indefinitely.

A pull request whose commits aren't all signed off can't be merged.

## Adding a design

1. Copy `designs/_template` to `designs/<design-slug>` (lowercase letters,
   digits and dashes, e.g. `m18-to-20v-max-adapter`).
2. Fill in `design.yml` and `README.md`.
3. Add the model files: `.stl`, `.3mf` or `.step`, each under 50 MB.
4. Add at least one photo or render (`.jpg`, `.png` or `.webp`, under 5 MB)
   to `photos/`.
5. Open a pull request and tick the checklist.

The `validate` check runs `scripts/validate.py` on every pull request; you can
run it yourself with `python3 scripts/validate.py`.

## Changing a design

Edit its files in place and bump `version` in `design.yml`. A maintainer tags
the merge as `<design-slug>/v<version>`. Only a design's creator may change it;
other improvements are a new design.

## Battery adapters

A design that lists a battery platform must fill in `safety:` saying what
protection the adapter does or doesn't keep (e.g. low-voltage cutoff, thermal
cutoff) and the current it was tested at. Adapters without it aren't merged.

## Takedowns

If something here is yours and was submitted by someone else, open an issue or
email the maintainers. It's removed from the current tree, and devicejuju
stops linking to it.
