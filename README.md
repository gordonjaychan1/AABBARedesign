# AABBA Redesign

A redesign concept for the [All American Black Belt Academy](https://www.aabbakarateacademy.com/) website (San Ramon, CA).
Plain HTML/CSS/JS, no framework and no build step needed to host it.

## Run locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000/index.html
```

## Editing content

Pages are generated from `tools/build.py`. Schedule, instructors and calendar data live at the top of that file; news posts live in `data/news.json`.

Links leave off `.html` (for example `classes` instead of `classes.html`). GitHub Pages serves both, but `python3 -m http.server` does not, so menu links 404 when previewing that way.

```bash
python3 tools/build.py
```

## What changed vs. the current site

| Issue on current site | Fix |
| --- | --- |
| Welcome text hard to read over the belt photo | Full-bleed hero with a dark gradient overlay and white text |
| Plain body font | Shippori Mincho (headings) + Inter (body) |
| Shadow on "free class" call-out; address in a different font | Flat call-out band; one type system throughout |
| Email/phone not vertically centered | Flex-aligned icon rows |
| `/copy-of-classes` URL | Clean `classes.html`, `news.html`, `instructors.html`, `calendar.html` |
| Class photos can't be browsed | Slideshow with arrows, swipe and arrow-key support |
| News page disorganized | Grouped by year, category filters, medal counts, duplicates removed |
| Slow photos | Every photo requested at display size, lazy-loaded, explicit dimensions |

## Notes

- Photos are the site's own copies in `assets/img/` (large) and `assets/img/sm/` (small), made from the originals downloaded from Wix. To redo them: `python3 tools/make_web_images.py "<folder of originals>"`. `tools/media_manifest.py` lists every photo and video and its file name.
- The kata videos still play from Wix until they're moved to a YouTube channel for the dojo.
- The Media page is left out of this redesign.
- Content is copied from the current site as of 2026-09-29; verify before publishing.

## Belt tests

The Belt Tests page unlocks each belt's written test in the browser with that belt's password. The published files in `assets/tests/` are encrypted (AES-256 with a key derived from the password via PBKDF2), so the PDFs can't be read without the password even though the repo is public.

Passwords and original PDFs live in `tests-private/`, which is git-ignored. **Never commit that folder.**

1. Put each test PDF in `tests-private/sources/`.
2. List the belts in `tests-private/belts.json`: `[{"id": "kyu9", "label": "9th Kyu", "pdf": "sources/kyu9.pdf", "password": "three-random-words"}]`
3. Lock them and rebuild:

```bash
python3 tools/encrypt_tests.py && python3 tools/build.py
```

To change a password, edit it in `belts.json` and run step 3 again. `tools/make_sample_tests.py` creates placeholder tests for demos; each sample password is the rank plus "password" (for example `9kyupassword`, `shodanhopassword`). Passwords must match exactly, including capitals, spaces and hyphens.
