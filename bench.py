"""A1 data collection: crypto choices for a low-cost Bluetooth earbud chip.

Measures time (ms) for the earbud's side of each task:
  hashing    - hash a 512 KB firmware image          : SHA-256, SHA3-256, BLAKE2s
  symmetric  - encrypt 1000 x 1 KB audio frames       : AES-128-GCM, ChaCha20-Poly1305, 3DES-CBC
  asymmetric - verify the vendor signature on one
               SHA-256 firmware digest                : RSA-2048, ECDSA-P256, Ed25519
The vendor signs once on its own server, so signing is done outside the timer.

Fairness rules:
  - keys, signatures, nonces/IVs and 3DES padding are prepared before the timer starts,
    so each timed region holds only the cipher/hash/verify work
  - AEAD nonces are 96-bit frame counters (unique per key, as RFC 8439 and SP 800-38D require);
    3DES-CBC gets a fresh random IV per frame (SP 800-38A)
  - the order of the three algorithms is shuffled every round (seeded), so drift and
    background load do not always hit the same algorithm first

Usage: python3 bench.py LABEL [runs]
Writes data/time_<LABEL>.csv (one row per run) and data/env_<LABEL>.json (versions, load).
Analysis lives in analyze.py.

Set OPENSSL_ia32cap on x86 to switch off AES-NI / SHA-NI and mimic a chip
without crypto hardware (see README.md).
"""

import csv
import hashlib
import json
import os
import platform
import random
import ssl
import sys
import time
from pathlib import Path

import cryptography
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

LABEL = sys.argv[1] if len(sys.argv) > 1 else platform.node()
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
DATA = Path(__file__).parent / "data"
SEED = 2539
N_FRAMES = 1000

FIRMWARE = os.urandom(512 * 1024)
FRAMES = [os.urandom(1024) for _ in range(N_FRAMES)]
DIGEST = hashlib.sha256(FIRMWARE).digest()


def timed(fn):
    start = time.perf_counter()
    fn()
    return (time.perf_counter() - start) * 1000


# --- hashing --------------------------------------------------------------
HASHES = {
    "SHA-256": lambda: hashlib.sha256(FIRMWARE).digest(),
    "SHA3-256": lambda: hashlib.sha3_256(FIRMWARE).digest(),
    "BLAKE2s": lambda: hashlib.blake2s(FIRMWARE).digest(),
}

# --- symmetric ------------------------------------------------------------
aes = AESGCM(os.urandom(16))
chacha = ChaCha20Poly1305(os.urandom(32))
des3 = TripleDES(os.urandom(24))


def pkcs7(frame):
    p = padding.PKCS7(64).padder()
    return p.update(frame) + p.finalize()


PADDED = [pkcs7(f) for f in FRAMES]  # padding is fixed work, done once outside the timer


class Symmetric:
    """Holds per-run inputs so nonce/IV creation stays outside the timer."""

    def __init__(self):
        self.counter = 0
        self.nonces = []
        self.des3_ciphers = []

    def prepare(self):
        start = self.counter
        self.nonces = [(start + i).to_bytes(12, "big") for i in range(N_FRAMES)]
        self.counter += N_FRAMES
        self.des3_ciphers = [Cipher(des3, modes.CBC(os.urandom(8))) for _ in range(N_FRAMES)]

    def aead(self, cipher):
        for nonce, frame in zip(self.nonces, FRAMES):
            cipher.encrypt(nonce, frame, None)

    def triple_des(self):
        for c, data in zip(self.des3_ciphers, PADDED):
            enc = c.encryptor()
            enc.update(data) + enc.finalize()


SYM = Symmetric()
SYMMETRIC = {
    "AES-128-GCM": lambda: SYM.aead(aes),
    "ChaCha20-Poly1305": lambda: SYM.aead(chacha),
    "3DES-CBC": SYM.triple_des,
}

# --- asymmetric: the earbud verifies, the vendor signed once beforehand ----
PSS = rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.DIGEST_LENGTH)
_rsa = rsa.generate_private_key(public_exponent=65537, key_size=2048)
_ec = ec.generate_private_key(ec.SECP256R1())
_ed = ed25519.Ed25519PrivateKey.generate()
RSA_PUB, RSA_SIG = _rsa.public_key(), _rsa.sign(DIGEST, PSS, hashes.SHA256())
EC_PUB, EC_SIG = _ec.public_key(), _ec.sign(DIGEST, ec.ECDSA(hashes.SHA256()))
ED_PUB, ED_SIG = _ed.public_key(), _ed.sign(DIGEST)

ASYMMETRIC = {
    "RSA-2048": lambda: RSA_PUB.verify(RSA_SIG, DIGEST, PSS, hashes.SHA256()),
    "ECDSA-P256": lambda: EC_PUB.verify(EC_SIG, DIGEST, ec.ECDSA(hashes.SHA256())),
    "Ed25519": lambda: ED_PUB.verify(ED_SIG, DIGEST),
}

GROUPS = {"hashing": HASHES, "symmetric": SYMMETRIC, "asymmetric": ASYMMETRIC}


def environment():
    return {
        "label": LABEL,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "cryptography": cryptography.__version__,
        "cryptography_openssl": backend.openssl_version_text(),
        "hashlib_openssl": ssl.OPENSSL_VERSION,
        "blake2s_impl": type(hashlib.blake2s()).__module__ + "." + type(hashlib.blake2s()).__name__,
        "OPENSSL_ia32cap": os.environ.get("OPENSSL_ia32cap"),
        "load_avg_start": os.getloadavg() if hasattr(os, "getloadavg") else None,
        "runs": RUNS,
        "seed": SEED,
    }


def main():
    env = environment()
    rng = random.Random(SEED)
    rows = []
    for group, algos in GROUPS.items():
        if group == "symmetric":
            SYM.prepare()
        for fn in algos.values():  # warm-up so first-call costs don't skew run 1
            fn()
        for run in range(1, RUNS + 1):
            if group == "symmetric":
                SYM.prepare()
            order = list(algos)
            rng.shuffle(order)
            for position, name in enumerate(order, 1):
                rows.append({"machine": LABEL, "group": group, "algorithm": name, "run": run,
                             "position": position, "ms": timed(algos[name])})
    env["load_avg_end"] = os.getloadavg() if hasattr(os, "getloadavg") else None

    DATA.mkdir(exist_ok=True)
    out = DATA / f"time_{LABEL}.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["machine", "group", "algorithm", "run", "position", "ms"])
        w.writeheader()
        w.writerows(rows)
    (DATA / f"env_{LABEL}.json").write_text(json.dumps(env, indent=2) + "\n")
    print(f"{LABEL}: wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
