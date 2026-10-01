#!/usr/bin/env python3
"""Creates placeholder belt-test PDFs and a password for each, for demoing the Belt Tests page.

Writes tests-private/ (git-ignored): sources/<belt>.pdf and belts.json.
Replace the PDFs with the real tests and the passwords with Sensei Eric's, then run tools/encrypt_tests.py.
"""
import json
import pathlib
import secrets

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "tests-private"

BELTS = [("orange", "Orange Belt"), ("blue", "Blue Belt"), ("purple", "Purple Belt"),
         ("red", "Red Belt"), ("brown", "Brown Belt")]

WORDS = ("maple river tiger cedar falcon harbor lantern meadow pebble summit thunder willow "
         "anchor bamboo canyon dragon ember forest glacier island jasmine kettle lotus marble "
         "nectar orchid panther quartz raven saddle tulip valley walnut zephyr breeze comet").split()


def password():
    return "-".join(secrets.choice(WORDS) for _ in range(3))


def pdf(lines):
    """Smallest valid one-page PDF with the given lines of text."""
    def esc(s):
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    text = "BT /F1 16 Tf 72 720 Td 22 TL " + " ".join(f"({esc(l)}) '" for l in lines) + " ET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(text)} >>\nstream\n{text}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n" + "".join(f"{o:010d} 00000 n \n" for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return out.encode("latin-1")


if __name__ == "__main__":
    (PRIVATE / "sources").mkdir(parents=True, exist_ok=True)
    belts = []
    for bid, label in BELTS:
        path = PRIVATE / "sources" / f"{bid}.pdf"
        path.write_bytes(pdf([
            "All American Black Belt Academy",
            f"{label} Written Test",
            "",
            "SAMPLE - placeholder for the real test.",
            "",
            "1. What does the word \"karate\" mean?",
            "2. Name the kata required for this belt.",
            "3. What are the dojo's four traditional values?",
        ]))
        belts.append({"id": bid, "label": label, "pdf": f"sources/{bid}.pdf", "password": password()})
    (PRIVATE / "belts.json").write_text(json.dumps(belts, indent=1))
    print(f"wrote {len(belts)} sample tests and passwords to {PRIVATE.relative_to(ROOT)}/")
