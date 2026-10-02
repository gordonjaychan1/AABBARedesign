#!/usr/bin/env python3
"""Lists every Wix-hosted photo and video the site uses, with a readable file name for each."""
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402  (data only; build.py only writes pages when run directly)


def slug(s, n=48):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-")


def ext(media_id):
    m = re.search(r"\.(jpe?g|png)$", media_id, re.I)
    return "." + (m.group(1).lower().replace("jpeg", "jpg") if m else "jpg")


def photos():
    """[(wix media id, file name)] in a sensible order; an id used twice keeps its first name."""
    items = [(build.HERO, "welcome-belts"), (build.LOGO_FLAG, "logo-aabba"), (build.LOGO_FIST, "logo-hayashi-ha")]
    days = dict(build.DAYS + [("Sat", "Saturday")])
    items += [(m, f"day-{days[d].lower()}") for d, m in build.DAY_PHOTOS.items()]
    items += [(c[3], f"class-{slug(c[0])}") for c in build.CLASSES]
    items += [(m, f"slideshow-{i + 1}") for i, m in enumerate(build.SLIDESHOW)]
    items += [(img, f"instructor-{slug(name)}") for _, name, img, _ in build.INSTRUCTORS]
    items += [(n["photo"], f"news-{n['date']}-{slug(n['title'], 40)}") for n in build.NEWS]
    items += [(m, f"calendar-{slug(label)}") for label, m in build.CALENDAR]
    items += [(icon, f"icon-{slug(name)}") for name, _, icon in build.SOCIAL]
    items += [(f"{vid}f000.jpg", f"kata-poster-{slug(name)}") for name, vid in build.KATA]
    seen, out = set(), []
    for mid, name in items:
        if mid not in seen:
            seen.add(mid)
            out.append((mid, name + ext(mid)))
    return out


def videos():
    return [(vid, f"kata-{slug(name)}.mp4") for name, vid in build.KATA]


if __name__ == "__main__":
    p, v = photos(), videos()
    print(len(p), "photos,", len(v), "videos")
    for mid, name in p[:6] + p[-3:]:
        print(" ", name, "<-", mid)
