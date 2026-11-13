# A1 statistics

alpha = 0.05. H0: mean time is equal across the three algorithms in a group.

## Machine: mac-m-series

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.2252 | 0.0201 | 0.2192 | 1.13e-07 |
| SHA3-256 | 30 | 0.8331 | 0.0404 | 0.8256 | 0.0065 |
| BLAKE2s | 30 | 0.8741 | 0.0303 | 0.8717 | 0.0195 |

- One-way ANOVA: F = 4022.53, p = 1.89e-86 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.000123 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 4.7e-92
- Kruskal-Wallis (no normality assumed): H = 65.84, p = 5.04e-15
- Effect size eta^2 = 0.989 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 6.84e-06 (different)
- Games-Howell SHA-256 vs SHA3-256: p = 0 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 0.000129 (different)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 0.8709 | 0.0629 | 0.8549 | 4.72e-06 |
| ChaCha20-Poly1305 | 30 | 1.5607 | 0.1116 | 1.5314 | 4.53e-06 |
| 3DES-CBC | 30 | 63.9696 | 4.4473 | 62.6715 | 3.21e-05 |

- One-way ANOVA: F = 5968.82, p = 7.69e-94 -> **reject H0**
- Levene, median-centred (equal variance): p = 8.81e-08 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 3.69e-67
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.993 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0.554 (no significant difference)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)

### Asymmetric: verify the vendor signature on one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 0.0366 | 0.0030 | 0.0354 | 1.79e-06 |
| ECDSA-P256 | 30 | 0.0696 | 0.0139 | 0.0656 | 9.21e-10 |
| Ed25519 | 30 | 0.2041 | 0.0106 | 0.2002 | 2.87e-08 |

- One-way ANOVA: F = 2240.18, p = 1.49e-75 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.279 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 3.15e-60
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.981 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 0 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 1.78e-13 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 0 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 4.66e-15 (different)

## Machine: omen-ryzen

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.2845 | 0.0157 | 0.2766 | 2.49e-05 |
| SHA3-256 | 30 | 1.0778 | 0.0999 | 1.0278 | 4.97e-07 |
| BLAKE2s | 30 | 1.1296 | 0.0571 | 1.1023 | 2.54e-06 |

- One-way ANOVA: F = 1498.09, p = 3.96e-68 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.0195 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 2.75e-78
- Kruskal-Wallis (no normality assumed): H = 65.99, p = 4.67e-15
- Effect size eta^2 = 0.972 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 0.00999 (different)
- Games-Howell SHA-256 vs SHA3-256: p = 0 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 1.11e-15 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 0.0452 (different)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 0.9132 | 0.0546 | 0.8899 | 2.82e-05 |
| ChaCha20-Poly1305 | 30 | 1.2333 | 0.0787 | 1.2070 | 7.15e-05 |
| 3DES-CBC | 30 | 36.5167 | 1.8991 | 36.0545 | 1.45e-06 |

- One-way ANOVA: F = 10423.69, p = 2.58e-104 -> **reject H0**
- Levene, median-centred (equal variance): p = 6.04e-06 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 2.42e-61
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.996 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0.499 (no significant difference)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 1.67e-15 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)

### Asymmetric: verify the vendor signature on one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 0.0267 | 0.0031 | 0.0255 | 7.05e-06 |
| ECDSA-P256 | 30 | 0.0651 | 0.0027 | 0.0639 | 7.89e-06 |
| Ed25519 | 30 | 0.1052 | 0.0088 | 0.1014 | 7.74e-08 |

- One-way ANOVA: F = 1481.17, p = 6.4e-68 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.074 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 8.79e-71
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.971 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 0 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 1.47e-14 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 0 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 0 (different)

## Machine: omen-no-crypto-hw

### Hashing: 512 KB firmware image

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| SHA-256 | 30 | 0.9800 | 0.0135 | 0.9833 | 0.208 |
| SHA3-256 | 30 | 1.1185 | 0.0364 | 1.1115 | 3.3e-05 |
| BLAKE2s | 30 | 1.1780 | 0.0199 | 1.1828 | 0.0612 |

- One-way ANOVA: F = 487.16, p = 5.56e-48 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.0527 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 9.39e-55
- Kruskal-Wallis (no normality assumed): H = 72.57, p = 1.75e-16
- Effect size eta^2 = 0.918 (large)
- Tukey SHA-256 vs SHA3-256: p = 0 (different)
- Tukey SHA-256 vs BLAKE2s: p = 0 (different)
- Tukey SHA3-256 vs BLAKE2s: p = 4.62e-14 (different)
- Games-Howell SHA-256 vs SHA3-256: p = 1.55e-15 (different)
- Games-Howell SHA-256 vs BLAKE2s: p = 0 (different)
- Games-Howell SHA3-256 vs BLAKE2s: p = 1.77e-09 (different)

### Symmetric: 1000 x 1 KB audio frames

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| AES-128-GCM | 30 | 3.8478 | 0.1153 | 3.8014 | 2.25e-05 |
| ChaCha20-Poly1305 | 30 | 1.1983 | 0.0400 | 1.1951 | 0.0175 |
| 3DES-CBC | 30 | 35.6249 | 1.0031 | 35.3772 | 0.0187 |

- One-way ANOVA: F = 32348.87, p = 1.17e-125 -> **reject H0**
- Levene, median-centred (equal variance): p = 7.18e-11 -> variances differ
- Alexander-Govern (unequal-variance robust): p = 3.12e-109
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.999 (large)
- Tukey AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Tukey AES-128-GCM vs 3DES-CBC: p = 0 (different)
- Tukey ChaCha20-Poly1305 vs 3DES-CBC: p = 0 (different)
- Games-Howell AES-128-GCM vs ChaCha20-Poly1305: p = 0 (different)
- Games-Howell AES-128-GCM vs 3DES-CBC: p = 3.89e-15 (different)
- Games-Howell ChaCha20-Poly1305 vs 3DES-CBC: p = 1.67e-15 (different)

### Asymmetric: verify the vendor signature on one firmware digest

| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |
|---|---|---|---|---|---|
| RSA-2048 | 30 | 0.0302 | 0.0065 | 0.0281 | 2.16e-07 |
| ECDSA-P256 | 30 | 0.0674 | 0.0032 | 0.0673 | 0.0913 |
| Ed25519 | 30 | 0.1059 | 0.0065 | 0.1046 | 6.72e-06 |

- One-way ANOVA: F = 1355.54, p = 2.7e-66 -> **reject H0**
- Levene, median-centred (equal variance): p = 0.481 -> variances similar
- Alexander-Govern (unequal-variance robust): p = 2.99e-45
- Kruskal-Wallis (no normality assumed): H = 79.12, p = 6.59e-18
- Effect size eta^2 = 0.969 (large)
- Tukey RSA-2048 vs ECDSA-P256: p = 0 (different)
- Tukey RSA-2048 vs Ed25519: p = 0 (different)
- Tukey ECDSA-P256 vs Ed25519: p = 0 (different)
- Games-Howell RSA-2048 vs ECDSA-P256: p = 0 (different)
- Games-Howell RSA-2048 vs Ed25519: p = 2.46e-14 (different)
- Games-Howell ECDSA-P256 vs Ed25519: p = 2.66e-15 (different)
