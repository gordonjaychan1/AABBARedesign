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

Each rank on the Belt Tests page has its own password, which unlocks that rank's written test and/or requirements sheet in the browser. The published files in `assets/tests/` are encrypted (AES-256 with a key derived from the password via PBKDF2), so they can't be read without the password even though the repo is public.

Passwords and original PDFs live in `tests-private/`, which is git-ignored. **Never commit that folder.**

1. Convert the Word documents to PDF (macOS). This keeps their question numbers, answer letters and indents:
   ```bash
   python3 tools/docx_to_pdf.py "Some Doc.docx" tests-private/sources/kyu8-test.pdf --fix "typo=>fixed"
   ```
2. List the ranks in `tests-private/belts.json`:
   `[{"id": "kyu8", "label": "8th Kyu – Blue Belt", "password": "...", "files": [{"kind": "test", "label": "Written Test", "pdf": "sources/kyu8-test.pdf"}, {"kind": "requirements", "label": "Requirements", "pdf": "sources/kyu8-requirements.pdf"}]}]`
3. Lock them and rebuild:
   ```bash
   python3 tools/encrypt_tests.py && python3 tools/build.py
   ```

To change a password, edit it in `belts.json` and run step 3 again. Passwords must match exactly, including capitals.

Corrections to the tests' wording (typos etc.) are listed in `tests-private/fixes.json`. After changing that list or getting new Word files, rebuild every PDF with `python3 tools/rebuild_test_pdfs.py` (it reads `~/Desktop/aabbaBeltReqs` by default), then run step 3.

### Online written tests

Ranks with a written test also get a "Take the Written Test Online" form. Its questions live in `tests-private/forms/<rank>.json` (locked like the PDFs) and are listed in `belts.json` with `"kind": "form"`. Answers are emailed to Sensei through [Web3Forms](https://web3forms.com); set its access key in `FORM_ACCESS_KEY` in `tools/build.py` and rebuild. Until a key is set, students can still fill in the test and download their answers. Answers are saved in the student's browser as they type and cleared after sending.
