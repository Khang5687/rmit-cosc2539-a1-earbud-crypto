# Cryptography cost on budget Bluetooth earbuds

Code and data for COSC2539 Assessment 1 (RMIT University Vietnam). The benchmark compares three hashing, three symmetric and three asymmetric algorithms on earbud-style workloads and tests the differences with one-way ANOVA.

| File | Does |
|---|---|
| `bench.py LABEL [runs]` | Times the nine algorithms in interleaved rounds (default 30) and writes `data/time_LABEL.csv` |
| `sizes.py` | Measures digest size, per-frame overhead, signature and public key size, and compares them with a 244-byte BLE payload; writes `data/sizes.csv` |
| `analyze.py` | Shapiro-Wilk, Levene, ANOVA, Alexander-Govern, Kruskal-Wallis, eta squared, Tukey HSD and Games-Howell; writes `results/stats.md` and the charts in `results/` |
| `demo.py` | Three-scene demonstration: a tampered firmware image fails the hash check, an edited audio frame fails the AEAD tag, and attacker-signed firmware fails the signature check |

## Setups in the data

- `mac-m-series`: Apple M1 Pro, Python 3.12.10, cryptography 46.0.5, OpenSSL 3.5.5
- `omen-ryzen`: AMD Ryzen 5 5600H, Ubuntu (Linux 6.8), Python 3.12.3, cryptography 50.0.2, OpenSSL 4.0.3
- `omen-no-crypto-hw`: the same Ryzen machine with AES-NI, PCLMULQDQ and SHA-NI hidden from OpenSSL:
  `OPENSSL_ia32cap="~0x200000200000000:~0x20000000" python3 bench.py omen-no-crypto-hw`

## Run it

pip install cryptography pandas scipy matplotlib
pip install cryptography pandas scipy statsmodels matplotlib
python3 bench.py my-machine 30
python3 sizes.py
python3 analyze.py
python3 demo.py
```
