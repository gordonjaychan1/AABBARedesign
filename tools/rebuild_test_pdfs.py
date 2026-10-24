#!/usr/bin/env python3
"""Rebuilds every belt test / requirements PDF from Sensei Laura's Word files, applying the saved
corrections in tests-private/fixes.json ([["old", "new"], ...]). Then run tools/encrypt_tests.py.

Usage: python3 tools/rebuild_test_pdfs.py [folder of Word files]   (default: ~/Desktop/aabbaBeltReqs)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import docx_to_pdf  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "tests-private"

if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / "Desktop" / "aabbaBeltReqs"
    fixes = [tuple(f) for f in json.loads((PRIVATE / "fixes.json").read_text(encoding="utf-8"))]
    n = 0
    for rank in json.loads((PRIVATE / "belts.json").read_text(encoding="utf-8")):
        for f in rank["files"]:
            if f["kind"] == "form": continue
            docx_to_pdf.convert(str(src / f["from"]), str(PRIVATE / f["pdf"]), fixes)
            n += 1
    print(f"rebuilt {n} PDFs with {len(fixes)} corrections")
