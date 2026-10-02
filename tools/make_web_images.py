#!/usr/bin/env python3
"""Makes web-sized copies of the original photos for the site (macOS `sips` does the resizing).

Usage: python3 tools/make_web_images.py "<folder of originals>"
Writes assets/img/<name> (up to 1600px wide), assets/img/sm/<name> (up to 720px wide),
and data/media.json, which maps each old Wix media id to its file name for tools/build.py.
"""
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import media_manifest as mm  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LARGE, SMALL = 1600, 720


def width(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", str(path)], capture_output=True, text=True, check=True).stdout
    return int(out.split("pixelWidth:")[1].split()[0])


def resize(src, dest, max_w):
    dest.parent.mkdir(parents=True, exist_ok=True)
    args = ["sips", str(src), "--out", str(dest)]
    if width(src) > max_w:
        args += ["--resampleWidth", str(max_w)]
    if dest.suffix == ".jpg":
        args += ["-s", "format", "jpeg", "-s", "formatOptions", "72"]
    if len(args) == 4:  # nothing to resize or convert; sips writes no file in that case
        shutil.copyfile(src, dest)
        return
    subprocess.run(args, capture_output=True, check=True)
    if dest.stat().st_size > src.stat().st_size:  # never ship something bigger than the original
        shutil.copyfile(src, dest)


if __name__ == "__main__":
    originals = pathlib.Path(sys.argv[1])
    out = ROOT / "assets" / "img"
    if out.exists():
        shutil.rmtree(out)
    mapping = {}
    for mid, name in mm.photos():
        src = originals / name
        resize(src, out / name, LARGE)
        resize(src, out / "sm" / name, SMALL)
        mapping[mid] = name
    (ROOT / "data" / "media.json").write_text(json.dumps(mapping, indent=1))
    total = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"{len(mapping)} photos -> assets/img ({total / 1e6:.1f} MB)")
