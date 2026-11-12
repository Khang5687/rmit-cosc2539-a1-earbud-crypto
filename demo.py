"""A1 live demo: the three crypto families stopping the earbud attacks.

Scene 1 (hashing)    - Airoha worm rewrites firmware -> hash check catches it
Scene 2 (symmetric)  - attacker sniffs / edits an audio frame -> unreadable, edit rejected
Scene 3 (asymmetric) - vendor-signed firmware installs, attacker-signed firmware refused

Usage: python3 demo.py   (pauses between scenes; press Enter to continue)
"""

import hashlib
import os
import sys

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

GREEN, RED, BOLD, END = "\033[92m", "\033[91m", "\033[1m", "\033[0m"


def ok(msg):
    print(f"  {GREEN}ACCEPT{END}  {msg}")


def bad(msg):
    print(f"  {RED}REJECT{END}  {msg}")


def pause(title):
    if sys.stdin.isatty():
        input(f"\n{BOLD}[Enter] {title}{END}")
    else:
        print(f"\n{BOLD}== {title} =={END}")


def flip_one_byte(data, index):
    return data[:index] + bytes([data[index] ^ 0x01]) + data[index + 1:]


firmware = b"EARBUD-FW v2.4.1\n" + os.urandom(64 * 1024)
tampered = flip_one_byte(firmware, 40_000)


def scene_hash():
    pause("Scene 1 - Hashing: did anyone change the firmware?")
    trusted = hashlib.sha256(firmware).hexdigest()
    print(f"  Vendor publishes SHA-256: {trusted[:32]}...")
    for label, image in [("original firmware", firmware), ("worm-modified firmware (1 byte flipped)", tampered)]:
        h = hashlib.sha256(image).hexdigest()
        print(f"  {label:<42} -> {h[:32]}...")
        (ok if h == trusted else bad)(label)
    print("  Limit: an attacker who can rewrite the firmware can also rewrite a plain hash. Scene 3 fixes that.")


def scene_symmetric():
    pause("Scene 2 - Symmetric: can a nearby attacker read or edit the audio link?")
    key = os.urandom(32)  # agreed during pairing (ECDH in real BLE / Fast Pair)
    link = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    frame = b"[mic audio] meeting at 3pm, door code 4821"
    sealed = link.encrypt(nonce, frame, None)
    print(f"  Plain frame : {frame!r}")
    print(f"  On the air  : {sealed[:32].hex()}...  (what a sniffer sees)")
    ok(f"earbud decrypts: {link.decrypt(nonce, sealed, None)!r}")
    try:
        link.decrypt(nonce, flip_one_byte(sealed, 5), None)
        ok("edited frame")
    except InvalidTag:
        bad("attacker flipped 1 bit in the frame -> Poly1305 tag check fails")
    try:
        ChaCha20Poly1305(os.urandom(32)).decrypt(nonce, sealed, None)
        ok("attacker key")
    except InvalidTag:
        bad("attacker without the pairing key cannot decrypt")


def scene_asymmetric():
    pause("Scene 3 - Asymmetric: only the vendor may sign firmware")
    vendor = ed25519.Ed25519PrivateKey.generate()
    attacker = ed25519.Ed25519PrivateKey.generate()
    burned_in_key = vendor.public_key()  # stored in the earbud at the factory
    digest = hashlib.sha256(firmware).digest()
    for label, image, signer in [
        ("vendor update, vendor signature", firmware, vendor),
        ("worm firmware, original vendor signature", tampered, vendor),
        ("worm firmware, attacker's own signature", tampered, attacker),
    ]:
        signature = signer.sign(digest)  # signer signs the genuine digest
        try:
            burned_in_key.verify(signature, hashlib.sha256(image).digest())
            ok(label)
        except InvalidSignature:
            bad(label)
    print(f"  Ed25519 signature = {len(vendor.sign(digest))} bytes: fits in one BLE packet (244 B). RSA-2048 = 256 bytes does not.")


if __name__ == "__main__":
    print(f"{BOLD}Earbud firmware + link security demo{END}")
    scene_hash()
    scene_symmetric()
    scene_asymmetric()
    print(f"\n{BOLD}Done.{END}")
