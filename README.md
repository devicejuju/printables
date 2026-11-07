# devicejuju printables

3D-printable designs for the devices in the [devicejuju](https://devicejuju.com)
catalog: wall mounts, holders, battery adapters, replacement knobs and the like.
Each design lists the devices and battery platforms it fits, and devicejuju shows
it on those devices' pages.

Everything here is dedicated to the public domain under
[CC0 1.0](LICENSE). Print it, sell prints, remix it — no permission or credit
needed.

## Layout

```
designs/
  <design-slug>/
    design.yml      # what it is and what it fits (required)
    README.md       # print settings, assembly, notes (required)
    *.stl / *.3mf / *.step
    photos/         # at least one photo or render (required)
```

A design's history is its git history; a release is a tag named
`<design-slug>/v<version>` (e.g. `trimmer-wall-mount/v2`).

## Contributing

Only original designs, by the person submitting them, dedicated to CC0. See
[CONTRIBUTING.md](CONTRIBUTING.md) — every commit needs a `Signed-off-by` line
agreeing to the creator certificate there.

## Safety

These designs are untested by devicejuju and come with no warranty. Battery
adapters in particular can bypass a tool's protection circuits and cause fires
or injury. Print and use them at your own risk.
