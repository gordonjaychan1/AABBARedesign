#!/usr/bin/env python3
"""Locks each rank's documents (written test, requirements) with that rank's password for the Belt Tests page.

Reads tests-private/belts.json:
  [{id, label, password, files: [{kind, label, pdf}]}]   (pdf paths are relative to tests-private/)
and writes:
  assets/tests/<id>-<kind>.bin   encrypted PDF (safe to publish)
  data/tests.json                ranks and their documents shown on the page (no passwords)

Format of each .bin: b"AABBA1" | salt (16) | iv (16) | HMAC-SHA256 (32) | AES-256-CBC ciphertext.
Keys come from PBKDF2-SHA256(password, salt); the first 32 bytes encrypt, the last 32 sign.
All of a rank's files share one salt, so the browser derives the key once per unlock.
js/tests.js reverses this. Passwords must match exactly, including capitals, spaces and hyphens.
"""
import hashlib
import hmac
import json
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "tests-private"
MAGIC = b"AABBA1"
ITERATIONS = 600_000


def normalize(pw):
    return pw  # exact match; kept as one place to change the rule (js/tests.js must match)


def derive(password, salt):
    key = hashlib.pbkdf2_hmac("sha256", normalize(password).encode(), salt, ITERATIONS, 64)
    return key[:32], key[32:]


def encrypt(data, salt, keys):
    enc_key, mac_key = keys
    iv = os.urandom(16)
    ct = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-K", enc_key.hex(), "-iv", iv.hex()],
                        input=data, capture_output=True, check=True).stdout
    tag = hmac.new(mac_key, MAGIC + salt + iv + ct, hashlib.sha256).digest()
    return MAGIC + salt + iv + tag + ct


if __name__ == "__main__":
    ranks = json.loads((PRIVATE / "belts.json").read_text())
    out = ROOT / "assets" / "tests"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.bin"):
        old.unlink()
    manifest, count = [], 0
    for r in ranks:
        salt = os.urandom(16)
        keys = derive(r["password"], salt)
        files = []
        for f in r["files"]:
            name = f"{r['id']}-{f['kind']}.bin"
            (out / name).write_bytes(encrypt((PRIVATE / f["pdf"]).read_bytes(), salt, keys))
            files.append({"kind": f["kind"], "label": f["label"], "file": f"assets/tests/{name}"})
            count += 1
        manifest.append({"id": r["id"], "label": r["label"], "iterations": ITERATIONS, "files": files})
    (ROOT / "data" / "tests.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print(f"locked {count} documents for {len(manifest)} ranks")
