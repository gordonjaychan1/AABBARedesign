#!/usr/bin/env python3
"""Converts a simple Word document (text, numbered/lettered lists, bold/italic/underline, centering,
tabs, divider lines) to a US Letter PDF that keeps its list numbers and indents.

macOS's built-in converter (textutil) turns Word's numbered lists into plain bullets, which loses the
question numbers and answer letters the belt tests rely on, so this reads the Word file itself and
lays the text out with macOS AppKit (tools/layout_to_pdf.js).

Usage: python3 tools/docx_to_pdf.py <in.docx> <out.pdf> [--fix "old=>new" ...]
"""
import json
import pathlib
import subprocess
import tempfile
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def attr(el, name):
    return None if el is None else el.get(W + name)


def roman(n):
    out = ""
    for v, s in [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]:
        while n >= v:
            out += s; n -= v
    return out


def letters(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(97 + r) + s
    return s


def fmt(n, kind):
    return {"decimal": str(n), "lowerLetter": letters(n), "upperLetter": letters(n).upper(),
            "lowerRoman": roman(n), "upperRoman": roman(n).upper()}.get(kind, str(n))


def numbering(z):
    """numId -> {level: (format, text pattern, start, (left indent pt, hanging pt))}"""
    try:
        root = ET.fromstring(z.read("word/numbering.xml"))
    except KeyError:
        return {}
    abstract = {}
    for a in root.findall(W + "abstractNum"):
        levels = {}
        for lvl in a.findall(W + "lvl"):
            ind = lvl.find(f"{W}pPr/{W}ind")
            levels[int(attr(lvl, "ilvl"))] = (attr(lvl.find(W + "numFmt"), "val") or "decimal",
                                             attr(lvl.find(W + "lvlText"), "val") or "",
                                             int(attr(lvl.find(W + "start"), "val") or 1),
                                             (int(attr(ind, "left") or attr(ind, "start") or 0) / 20, int(attr(ind, "hanging") or 0) / 20))
        abstract[attr(a, "abstractNumId")] = levels
    nums = {}
    for n in root.findall(W + "num"):
        levels = dict(abstract.get(attr(n.find(W + "abstractNumId"), "val"), {}))
        for o in n.findall(W + "lvlOverride"):
            lv = int(attr(o, "ilvl")); so = o.find(W + "startOverride")
            if so is not None and lv in levels:
                f, t, _, ind = levels[lv]; levels[lv] = (f, t, int(attr(so, "val")), ind)
        nums[attr(n, "numId")] = levels
    return nums



def runs(p, fixes, default_size):
    out = []
    for r in p.iter(W + "r"):
        rpr = r.find(W + "rPr")
        on = lambda tag: rpr is not None and rpr.find(W + tag) is not None and attr(rpr.find(W + tag), "val") not in ("0", "false", "none")
        size = attr(rpr.find(W + "sz"), "val") if rpr is not None else None
        text = ""
        for c in r:
            if c.tag == W + "t": text += c.text or ""
            elif c.tag == W + "tab": text += "\t"
            elif c.tag in (W + "br", W + "cr"): text += " "
        if not text: continue
        run = {"text": text, "b": on("b"), "i": on("i"), "u": on("u"), "size": int(size) / 2 if size else default_size}
        same = out and all(out[-1][k] == run[k] for k in ("b", "i", "u", "size"))
        if same: out[-1]["text"] += text  # Word often splits words into same-looking pieces
        else: out.append(run)
    for a, b in fixes:
        for run in out: run["text"] = run["text"].replace(a, b)
        joined = "".join(r["text"] for r in out)
        # still split across differently formatted pieces? (ignore spots already fixed, e.g. "first" -> "first?")
        if a in joined.replace(b, "\0") and out:
            out[0]["text"], rest = joined.replace(a, b), out[1:]
            for r in rest: r["text"] = ""
            out = [r for r in out if r["text"]]
    return out


def styles(z):
    """paragraph style id -> {"left", "hang", "jc", "size"}, following basedOn chains"""
    try:
        st = ET.fromstring(z.read("word/styles.xml"))
    except KeyError:
        return {}
    raw = {}
    for el in st.findall(W + "style"):
        if attr(el, "type") != "paragraph": continue
        ind = el.find(f"{W}pPr/{W}ind"); jc = el.find(f"{W}pPr/{W}jc"); sz = el.find(f"{W}rPr/{W}sz")
        raw[attr(el, "styleId")] = {"based": attr(el.find(W + "basedOn"), "val"),
                                    "left": int(attr(ind, "left") or attr(ind, "start") or 0) / 20 if ind is not None else None,
                                    "hang": int(attr(ind, "hanging") or 0) / 20 if ind is not None else None,
                                    "jc": attr(jc, "val"), "size": int(attr(sz, "val")) / 2 if sz is not None else None}
    def resolve(sid, seen=()):
        s = raw.get(sid)
        if not s or sid in seen: return {}
        base = resolve(s["based"], seen + (sid,))
        return {k: s[k] if s[k] is not None else base.get(k) for k in ("left", "hang", "jc", "size")}
    return {sid: resolve(sid) for sid in raw}


def default_size(z):
    try:
        st = ET.fromstring(z.read("word/styles.xml"))
    except KeyError:
        return 12
    normal = styles(z).get("Normal", {}).get("size")
    if normal: return normal
    el = st.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr/{W}sz")
    return int(attr(el, "val")) / 2 if el is not None else 12


def layout(path, fixes=()):
    z = zipfile.ZipFile(path)
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    nums = numbering(z)
    size = default_size(z)
    pstyles = styles(z)
    counters, paras = {}, []
    for p in body.iter(W + "p"):
        ppr = p.find(W + "pPr")
        sty = pstyles.get(attr(ppr.find(W + "pStyle"), "val") if ppr is not None else "Normal", {}) or pstyles.get("Normal", {})
        jc = (attr(ppr.find(W + "jc"), "val") if ppr is not None else None) or sty.get("jc")
        ind = ppr.find(W + "ind") if ppr is not None else None
        left = int(attr(ind, "left") or attr(ind, "start") or 0) / 20 if ind is not None else None
        hang = int(attr(ind, "hanging") or 0) / 20 if ind is not None else 0
        marker = ""
        num = ppr.find(W + "numPr") if ppr is not None else None
        if num is not None and attr(num.find(W + "numId"), "val") not in (None, "0"):
            nid = attr(num.find(W + "numId"), "val"); lvl = int(attr(num.find(W + "ilvl"), "val") or 0)
            levels = nums.get(nid, {})
            c = counters.setdefault(nid, {})
            c[lvl] = c.get(lvl, levels.get(lvl, ("", "", 1, (0, 0)))[2] - 1) + 1
            for deeper in [k for k in c if k > lvl]: del c[deeper]
            kind, pattern, _, (lvl_left, lvl_hang) = levels.get(lvl, ("decimal", "%1.", 1, (0, 0)))
            if kind == "bullet": marker = "•"
            elif kind != "none":
                marker = re.sub(r"%(\d)", lambda m: fmt(c.get(int(m.group(1)) - 1, levels.get(int(m.group(1)) - 1, ("", "", 1, (0, 0)))[2]),
                                                         levels.get(int(m.group(1)) - 1, ("decimal",))[0]), pattern)
            if left is None: left, hang = lvl_left, lvl_hang
        if left is None:  # Word precedence: paragraph, then list level, then paragraph style
            left, hang = sty.get("left"), sty.get("hang") or 0
        paras.append({"align": jc or "left", "left": left or 0, "hang": hang, "marker": marker, "runs": runs(p, fixes, size)})
        if ppr is not None and ppr.find(f"{W}pBdr/{W}bottom") is not None:  # divider line
            paras.append({"align": "left", "left": left or 0, "hang": 0, "marker": "", "runs": [{"text": "_" * 62, "b": False, "i": False, "u": False, "size": size}]})
    return {"size": size, "paragraphs": paras}


def convert(src, dest, fixes=()):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(layout(src, fixes), f)
    script = pathlib.Path(__file__).with_name("layout_to_pdf.js")
    out = subprocess.run(["osascript", "-l", "JavaScript", str(script), f.name, str(pathlib.Path(dest).resolve())], capture_output=True, text=True)
    pathlib.Path(f.name).unlink()
    if not out.stdout.startswith("ok"):
        raise SystemExit(f"PDF failed for {src}: {out.stdout}{out.stderr}")


if __name__ == "__main__":
    args = sys.argv[1:]
    fixes = [tuple(args[i + 1].split("=>", 1)) for i in range(2, len(args) - 1) if args[i] == "--fix"]
    convert(args[0], args[1], fixes)
