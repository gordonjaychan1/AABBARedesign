#!/usr/bin/env python3
"""Locks each belt test PDF with its belt's password for the Belt Tests page.

Reads tests-private/belts.json ([{id, label, pdf, password}]) and writes:
  assets/tests/<id>.bin    encrypted PDF (safe to publish)
  data/tests.json   list of belts shown on the page (no passwords)

Format of each .bin: b"AABBA1" | salt (16) | iv (16) | HMAC-SHA256 (32) | AES-256-CBC ciphertext.
Keys come from PBKDF2-SHA256(password, salt); the first 32 bytes encrypt, the last 32 sign.
js/tests.js reverses this in the browser. On both sides, passwords are lowercased with spaces and hyphens removed.
"""
import hashlib
import hmac
import json
import os
import re
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "tests-private"
MAGIC = b"AABBA1"
ITERATIONS = 600_000


def normalize(pw):
    return re.sub(r"[\s-]+", "", pw).lower()


def encrypt(data, password):
    salt, iv = os.urandom(16), os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", normalize(password).encode(), salt, ITERATIONS, 64)
    enc_key, mac_key = key[:32], key[32:]
    ct = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-K", enc_key.hex(), "-iv", iv.hex()],
                        input=data, capture_output=True, check=True).stdout
    tag = hmac.new(mac_key, MAGIC + salt + iv + ct, hashlib.sha256).digest()
    return MAGIC + salt + iv + tag + ct


if __name__ == "__main__":
    belts = json.loads((PRIVATE / "belts.json").read_text())
    out = ROOT / "assets" / "tests"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.bin"):
        old.unlink()
    manifest = []
    for b in belts:
        pdf = (PRIVATE / b["pdf"]).read_bytes()
        (out / f"{b['id']}.bin").write_bytes(encrypt(pdf, b["password"]))
        manifest.append({"id": b["id"], "label": b["label"], "file": f"assets/tests/{b['id']}.bin", "iterations": ITERATIONS})
    (ROOT / "data" / "tests.json").write_text(json.dumps(manifest, indent=1))
    print(f"locked {len(manifest)} tests")
