# A1 statistics

alpha = 0.05. H0: mean time is equal across the three algorithms in a group.

## Machine: mac-m-series

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.2630 | 0.1814 | 0.2269 | 2.07e-11 |
| SHA3-256 | 30 | 0.9266 | 0.1907 | 0.8346 | 4.33e-07 |
| BLAKE2s | 30 | 0.9758 | 0.1952 | 0.8965 | 1.16e-07 |

- One-way ANOVA: F = 132.85, p = 3.6e-27 -> **reject H0**
- Levene (equal variance): p = 0.315 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 2.98e-25
- Kruskal-Wallis (no normality assumed): H = 56.30, p = 5.95e-13
- Effect size eta^2 = 0.753 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 0.573 (no significant difference)
- Games-Howell SHA-256 vs SHA3-256: p = 2.22e-15 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 0.587 (no significant difference)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 2.1707 | 0.8318 | 1.9106 | 5.64e-10 |
| ChaCha20-Poly1305 | 30 | 3.0038 | 1.6544 | 2.6240 | 7.54e-11 |
| 3DES-CBC | 30 | 68.4203 | 6.2694 | 65.8192 | 8.97e-07 |

- One-way ANOVA: F = 3042.84, p = 3.04e-81 -> **reject H0**
- Levene (equal variance): p = 0.000595 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 1.41e-36
- Kruskal-Wallis (no normality assumed): H = 74.05, p = 8.34e-17
- Effect size eta^2 = 0.986 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0.67 (no significant difference)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 0.046 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 8.22e-15 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)

### Asymmetric: sign + verify one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 1.2262 | 0.1348 | 1.1744 | 4.99e-06 |
| ECDSA-P256 | 30 | 0.1626 | 0.0621 | 0.1407 | 5.38e-08 |
| Ed25519 | 30 | 0.3223 | 0.0259 | 0.3127 | 7.64e-07 |

- One-way ANOVA: F = 1304.79, p = 1.34e-65 -> **reject H0**
- Levene (equal variance): p = 0.00146 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 5.54e-38
- Kruskal-Wallis (no normality assumed): H = 74.50, p = 6.63e-17
- Effect size eta^2 = 0.968 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 9.13e-10 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 1.44e-15 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 0 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 1.33e-15 (different)

## Machine: omen-ryzen

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.2710 | 0.0137 | 0.2694 | 4.46e-08 |
| SHA3-256 | 30 | 1.0021 | 0.0290 | 1.0056 | 0.00435 |
| BLAKE2s | 30 | 1.0854 | 0.0456 | 1.0822 | 0.000181 |

- One-way ANOVA: F = 5821.08, p = 2.27e-93 -> **reject H0**
- Levene (equal variance): p = 0.000523 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 4.68e-103
- Kruskal-Wallis (no normality assumed): H = 76.98, p = 1.92e-17
- Effect size eta^2 = 0.993 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA-256 vs SHA3-256: p = 0 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 1.16e-10 (different)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 1.7450 | 0.0578 | 1.7181 | 3.18e-05 |
| ChaCha20-Poly1305 | 30 | 2.0339 | 0.0509 | 2.0177 | 0.00064 |
| 3DES-CBC | 30 | 36.6304 | 0.5237 | 36.4995 | 0.000238 |

- One-way ANOVA: F = 129231.91, p = 8.38e-152 -> **reject H0**
- Levene (equal variance): p = 6.7e-07 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 3.85e-81
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 1.000 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0.00124 (different)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)

### Asymmetric: sign + verify one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 0.5803 | 0.0220 | 0.5790 | 0.000771 |
| ECDSA-P256 | 30 | 0.0998 | 0.0040 | 0.0987 | 0.00273 |
| Ed25519 | 30 | 0.1331 | 0.0082 | 0.1314 | 2.41e-07 |

- One-way ANOVA: F = 11462.43, p = 4.21e-106 -> **reject H0**
- Levene (equal variance): p = 3.75e-06 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 1.25e-67
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.996 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 0 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 0 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 0 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 1.11e-16 (different)

## Machine: omen-no-crypto-hw

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.9135 | 0.0355 | 0.9068 | 3.2e-10 |
| SHA3-256 | 30 | 1.0292 | 0.0238 | 1.0238 | 8.01e-05 |
| BLAKE2s | 30 | 1.1003 | 0.0259 | 1.0937 | 7.23e-07 |

- One-way ANOVA: F = 320.41, p = 7.43e-41 -> **reject H0**
- Levene (equal variance): p = 0.959 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 1.39e-29
- Kruskal-Wallis (no normality assumed): H = 70.99, p = 3.84e-16
- Effect size eta^2 = 0.880 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA-256 vs SHA3-256: p = 0 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 0 (different)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 4.6076 | 0.0857 | 4.5921 | 0.0978 |
| ChaCha20-Poly1305 | 30 | 2.0958 | 0.0472 | 2.1007 | 0.16 |
| 3DES-CBC | 30 | 37.7074 | 1.3153 | 37.3841 | 3.31e-06 |

- One-way ANOVA: F = 20436.16, p = 5.39e-117 -> **reject H0**
- Levene (equal variance): p = 7.43e-06 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 5.51e-113
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.998 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 2.22e-15 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 6.11e-15 (different)

### Asymmetric: sign + verify one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 0.5928 | 0.0203 | 0.5902 | 0.00689 |
| ECDSA-P256 | 30 | 0.1059 | 0.0121 | 0.1012 | 2.1e-07 |
| Ed25519 | 30 | 0.1355 | 0.0116 | 0.1319 | 9.12e-07 |

- One-way ANOVA: F = 9665.17, p = 6.81e-103 -> **reject H0**
- Levene (equal variance): p = 0.0173 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 2.53e-82
- Kruskal-Wallis (no normality assumed): H = 76.74, p = 2.17e-17
- Effect size eta^2 = 0.996 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 1.21e-10 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 1.55e-15 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 0 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 2.99e-13 (different)
