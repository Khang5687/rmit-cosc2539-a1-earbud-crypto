"""A1 second variable: bytes on air.

For each algorithm, measures what it adds to a Bluetooth LE message:
  hashing    - digest size
  symmetric  - bytes added to one 1 KB audio frame (nonce/IV + padding + tag)
  asymmetric - signature size and public key size
and checks the result against one BLE packet's usable payload.

BLE_PAYLOAD = 244 bytes: max ATT payload with LE Data Length Extension
(251-byte link-layer payload, minus 4-byte L2CAP header and 3-byte ATT header; needs ATT_MTU >= 247).

Usage: python3 sizes.py   -> data/sizes.csv
"""

import csv
import hashlib
import os
from pathlib import Path

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

BLE_PAYLOAD = 244
SAMPLES = 30
OUT = Path(__file__).parent / "data" / "sizes.csv"
FRAME = os.urandom(1024)
DIGEST = hashlib.sha256(FRAME).digest()


def raw_pub(key):
    return len(key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo))


def main():
    rows = []

    def add(group, algo, metric, value):
        rows.append({"group": group, "algorithm": algo, "metric": metric, "bytes": value,
                     "fits_one_ble_packet": value <= BLE_PAYLOAD})

    add("hashing", "SHA-256", "digest", len(hashlib.sha256(FRAME).digest()))
    add("hashing", "SHA3-256", "digest", len(hashlib.sha3_256(FRAME).digest()))
    add("hashing", "BLAKE2s", "digest", len(hashlib.blake2s(FRAME).digest()))

    nonce = 12
    add("symmetric", "AES-128-GCM", "overhead_per_1KB_frame",
        nonce + len(AESGCM(os.urandom(16)).encrypt(os.urandom(nonce), FRAME, None)) - len(FRAME))
    add("symmetric", "ChaCha20-Poly1305", "overhead_per_1KB_frame",
        nonce + len(ChaCha20Poly1305(os.urandom(32)).encrypt(os.urandom(nonce), FRAME, None)) - len(FRAME))
    padder = padding.PKCS7(64).padder()
    padded = padder.update(FRAME) + padder.finalize()
    enc = Cipher(TripleDES(os.urandom(24)), modes.CBC(os.urandom(8))).encryptor()
    add("symmetric", "3DES-CBC", "overhead_per_1KB_frame", 8 + len(enc.update(padded) + enc.finalize()) - len(FRAME))

    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ec_key = ec.generate_private_key(ec.SECP256R1())
    ed_key = ed25519.Ed25519PrivateKey.generate()
    pss = rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.DIGEST_LENGTH)

    # ECDSA DER signatures vary by a few bytes, so report the largest of SAMPLES
    add("asymmetric", "RSA-2048", "signature", len(rsa_key.sign(DIGEST, pss, hashes.SHA256())))
    add("asymmetric", "ECDSA-P256", "signature",
        max(len(ec_key.sign(DIGEST, ec.ECDSA(hashes.SHA256()))) for _ in range(SAMPLES)))
    add("asymmetric", "Ed25519", "signature", len(ed_key.sign(DIGEST)))
    add("asymmetric", "RSA-2048", "public_key_der", raw_pub(rsa_key))
    add("asymmetric", "ECDSA-P256", "public_key_der", raw_pub(ec_key))
    add("asymmetric", "Ed25519", "public_key_der", raw_pub(ed_key))

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["group", "algorithm", "metric", "bytes", "fits_one_ble_packet"])
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['algorithm']:<18} {r['metric']:<24} {r['bytes']:>4} B  fits={r['fits_one_ble_packet']}")


if __name__ == "__main__":
    main()
