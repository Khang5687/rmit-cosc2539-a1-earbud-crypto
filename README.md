# Cryptography cost on budget Bluetooth earbuds

Code and data for COSC2539 Assessment 1 (RMIT University Vietnam). The benchmark compares three hashing, three symmetric and three asymmetric algorithms on earbud-style workloads and tests the differences with one-way ANOVA.

| File | Does |
|---|---|
| `bench.py LABEL [runs]` | Times the earbud's side of each task (hash a 512 KB firmware image, encrypt 1000 x 1 KB audio frames, verify one vendor signature) in rounds (default 30) with the algorithm order shuffled each round; writes `data/time_LABEL.csv` and `data/env_LABEL.json` |
| `sizes.py` | Measures digest size, per-frame overhead, signature and public key size, and compares them with a 244-byte BLE payload; writes `data/sizes.csv` |
| `analyze.py` | Shapiro-Wilk, Levene (median-centred), ANOVA, Alexander-Govern, Kruskal-Wallis, eta squared, Tukey HSD and Games-Howell; writes `results/stats.md` and the charts in `results/` |
| `demo.py` | Three-scene demonstration: a tampered firmware image fails the hash check, an edited audio frame fails the AEAD tag, and attacker-signed firmware fails the signature check |

Each timed region holds only the crypto work. Keys, the vendor signatures, the AEAD counter nonces, the 3DES IVs and the 3DES padding are prepared before the timer starts. `data/env_LABEL.json` records the Python and `cryptography` versions, the OpenSSL bundled in `cryptography`, the OpenSSL that `hashlib` links, the BLAKE2s implementation, `OPENSSL_ia32cap` and the load average.

## Setups in the data (run 2026-11-13)

- `mac-m-series`: Apple M1 Pro, Python 3.12.10, cryptography 46.0.5 (OpenSSL 3.5.5); hashlib on OpenSSL 3.0.16
- `omen-ryzen`: AMD Ryzen 5 5600H, Ubuntu 24.04 (Linux 6.8), Python 3.12.3, cryptography 50.0.2 (OpenSSL 4.0.3); hashlib on OpenSSL 3.0.13
- `omen-no-crypto-hw`: the same Ryzen machine with AES-NI, PCLMULQDQ and SHA-NI hidden from OpenSSL:
  `OPENSSL_ia32cap="~0x200000200000000:~0x20000000" python3 bench.py omen-no-crypto-hw`

BLAKE2s runs on CPython's own `_blake2` code on every setup, not on OpenSSL.

## Run it

```bash
pip install cryptography pandas scipy matplotlib
python3 bench.py my-machine 30
python3 sizes.py
python3 analyze.py
python3 demo.py
```
