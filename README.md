# AABBA Redesign

A redesign concept for the [All American Black Belt Academy](https://www.aabbakarateacademy.com/) website (San Ramon, CA).
Plain HTML/CSS/JS, no framework and no build step needed to host it.

## Run locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Editing content

Pages are generated from `tools/build.py` (schedule, news, instructors and calendar data live at the top of that file):

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
| `/copy-of-classes` URL | Clean `classes.html`, `news.html`, `media.html`, `instructors.html`, `calendar.html` |
| Class photos can't be browsed | Carousel with arrows, thumbnails, swipe and arrow-key support |
| News page disorganized | Grouped by year, category filters, medal counts, duplicates removed |
| Slow photos | Every photo requested at display size, lazy-loaded, explicit dimensions |

## Notes

- Photos are still served from the academy's existing Wix CDN, resized on the fly. For a production site, export originals and host optimized copies (WebP/AVIF).
- Kata videos on the Media page were not embedded on the original page in a scrapeable form; links need to come from the academy.
- Content is copied from the current site as of 2026-09-29; verify before publishing.
