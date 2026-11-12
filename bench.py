"""A1 data collection: crypto choices for a low-cost Bluetooth earbud chip.

Measures time (ms) per task, interleaved across algorithms:
  hashing    - hash a 512 KB firmware image          : SHA-256, SHA3-256, BLAKE2s
  symmetric  - encrypt 1000 x 1 KB audio frames       : AES-128-GCM, ChaCha20-Poly1305, 3DES-CBC
  asymmetric - sign + verify one firmware digest      : RSA-2048, ECDSA-P256, Ed25519

Usage: python3 bench.py LABEL [runs]
Writes data/time_<LABEL>.csv (one row per run). Analysis lives in analyze.py.

Set OPENSSL_ia32cap on x86 to switch off AES-NI / SHA-NI and mimic a chip
without crypto hardware (see README.md).
"""

import csv
import hashlib
import os
import platform
import sys
import time
from pathlib import Path

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

LABEL = sys.argv[1] if len(sys.argv) > 1 else platform.node()
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
OUT = Path(__file__).parent / "data" / f"time_{LABEL}.csv"

FIRMWARE = os.urandom(512 * 1024)
FRAMES = [os.urandom(1024) for _ in range(1000)]
DIGEST = hashlib.sha256(FIRMWARE).digest()


def timed(fn):
    start = time.perf_counter()
    fn()
    return (time.perf_counter() - start) * 1000


HASHES = {
    "SHA-256": lambda: hashlib.sha256(FIRMWARE).digest(),
    "SHA3-256": lambda: hashlib.sha3_256(FIRMWARE).digest(),
    "BLAKE2s": lambda: hashlib.blake2s(FIRMWARE).digest(),
}

aes = AESGCM(os.urandom(16))
chacha = ChaCha20Poly1305(os.urandom(32))
des3_key = os.urandom(24)


def run_aead(cipher):
    for frame in FRAMES:
        cipher.encrypt(os.urandom(12), frame, None)


def run_3des():
    for frame in FRAMES:
        enc = Cipher(TripleDES(des3_key), modes.CBC(os.urandom(8))).encryptor()
        padder = padding.PKCS7(64).padder()
        data = padder.update(frame) + padder.finalize()
        enc.update(data) + enc.finalize()


SYMMETRIC = {
    "AES-128-GCM": lambda: run_aead(aes),
    "ChaCha20-Poly1305": lambda: run_aead(chacha),
    "3DES-CBC": run_3des,
}

rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
ec_key = ec.generate_private_key(ec.SECP256R1())
ed_key = ed25519.Ed25519PrivateKey.generate()
PSS = rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH)


def rsa_sign_verify():
    sig = rsa_key.sign(DIGEST, PSS, hashes.SHA256())
    rsa_key.public_key().verify(sig, DIGEST, PSS, hashes.SHA256())


def ecdsa_sign_verify():
    sig = ec_key.sign(DIGEST, ec.ECDSA(hashes.SHA256()))
    ec_key.public_key().verify(sig, DIGEST, ec.ECDSA(hashes.SHA256()))


def ed_sign_verify():
    ed_key.public_key().verify(ed_key.sign(DIGEST), DIGEST)


ASYMMETRIC = {
    "RSA-2048": rsa_sign_verify,
    "ECDSA-P256": ecdsa_sign_verify,
    "Ed25519": ed_sign_verify,
}

GROUPS = {"hashing": HASHES, "symmetric": SYMMETRIC, "asymmetric": ASYMMETRIC}


def main():
    rows = []
    for group, algos in GROUPS.items():
        for fn in algos.values():  # warm-up so first-call costs don't skew run 1
            fn()
        for run in range(1, RUNS + 1):
            for name, fn in algos.items():  # interleave so background load hits all equally
                rows.append({"machine": LABEL, "group": group, "algorithm": name, "run": run, "ms": timed(fn)})

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["machine", "group", "algorithm", "run", "ms"])
        w.writeheader()
        w.writerows(rows)
    print(f"{LABEL}: wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
