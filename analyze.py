"""A1 analysis: ANOVA + assumption checks + effect size + charts.

Reads every data/time_*.csv, and per machine and group runs:
  - descriptive stats (mean, SD, median)
  - Shapiro-Wilk per algorithm (normality) and Levene, median-centred (equal variance)
  - one-way ANOVA (the method the course asks for)
  - Alexander-Govern test (robust to unequal variance) and Kruskal-Wallis (no normality)
  - eta squared (effect size: share of time variation explained by the algorithm)
  - Tukey HSD and Games-Howell pairwise
Writes results/stats.md and results/*.png.

Usage: python3 analyze.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
from scipy import stats

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "results"
ALPHA = 0.05
GROUP_TITLES = {
    "hashing": "Hashing: 512 KB firmware image",
    "symmetric": "Symmetric: 1000 x 1 KB audio frames",
    "asymmetric": "Asymmetric: verify the vendor signature on one firmware digest",
}
ALGOS = {
    "hashing": ["SHA-256", "SHA3-256", "BLAKE2s"],
    "symmetric": ["AES-128-GCM", "ChaCha20-Poly1305", "3DES-CBC"],
    "asymmetric": ["RSA-2048", "ECDSA-P256", "Ed25519"],
}


def games_howell(a, b, k):
    """Pairwise test that, unlike Tukey HSD, does not assume equal variances."""
    a, b = pd.Series(a), pd.Series(b)
    va, vb = a.var() / len(a), b.var() / len(b)
    q = abs(a.mean() - b.mean()) / ((va + vb) / 2) ** 0.5
    df = (va + vb) ** 2 / (va**2 / (len(a) - 1) + vb**2 / (len(b) - 1))
    return stats.studentized_range.sf(q, k, df)


def eta_squared(samples):
    values = [v for s in samples for v in s]
    grand = sum(values) / len(values)
    ss_between = sum(len(s) * (sum(s) / len(s) - grand) ** 2 for s in samples)
    ss_total = sum((v - grand) ** 2 for v in values)
    return ss_between / ss_total


def analyse(df):
    lines = ["# A1 statistics", "", f"alpha = {ALPHA}. H0: mean time is equal across the three algorithms in a group.", ""]
    for machine, mdf in df.groupby("machine", sort=False):
        lines += [f"## Machine: {machine}", ""]
        for group in GROUP_TITLES:
            gdf = mdf[mdf.group == group]
            algos = ALGOS[group]
            samples = [gdf[gdf.algorithm == a].ms.tolist() for a in algos]
            lines += [f"### {GROUP_TITLES[group]}", "", "| Algorithm | n | Mean ms | SD | Median ms | Shapiro p |", "|---|---|---|---|---|---|"]
            for a, s in zip(algos, samples):
                ser = pd.Series(s)
                lines.append(f"| {a} | {len(s)} | {ser.mean():.4f} | {ser.std():.4f} | {ser.median():.4f} | {stats.shapiro(s).pvalue:.3g} |")
            f_stat, p_anova = stats.f_oneway(*samples)
            lev = stats.levene(*samples)
            ag = stats.alexandergovern(*samples)
            kw = stats.kruskal(*samples)
            eta = eta_squared(samples)
            verdict = "reject H0" if p_anova < ALPHA else "keep H0"
            lines += [
                "",
                f"- One-way ANOVA: F = {f_stat:.2f}, p = {p_anova:.3g} -> **{verdict}**",
                f"- Levene, median-centred (equal variance): p = {lev.pvalue:.3g} -> {'variances differ' if lev.pvalue < ALPHA else 'variances similar'}",
                f"- Alexander-Govern (unequal-variance robust): p = {ag.pvalue:.3g}",
                f"- Kruskal-Wallis (no normality assumed): H = {kw.statistic:.2f}, p = {kw.pvalue:.3g}",
                f"- Effect size eta^2 = {eta:.3f} ({'large' if eta >= 0.14 else 'medium' if eta >= 0.06 else 'small'})",
            ]
            tukey = stats.tukey_hsd(*samples)
            for i in range(len(algos)):
                for j in range(i + 1, len(algos)):
                    p = tukey.pvalue[i][j]
                    lines.append(f"- Tukey {algos[i]} vs {algos[j]}: p = {p:.3g} ({'different' if p < ALPHA else 'no significant difference'})")
            for i in range(len(algos)):
                for j in range(i + 1, len(algos)):
                    p = games_howell(samples[i], samples[j], len(algos))
                    lines.append(f"- Games-Howell {algos[i]} vs {algos[j]}: p = {p:.3g} ({'different' if p < ALPHA else 'no significant difference'})")
            lines.append("")
    return "\n".join(lines)


SETUP_NAMES = {"mac-m-series": "Mac", "omen-ryzen": "Ryzen", "omen-no-crypto-hw": "Ryzen, no crypto hardware"}
SHORT = {"AES-128-GCM": "AES-GCM", "ChaCha20-Poly1305": "ChaCha20", "3DES-CBC": "3DES",
         "RSA-2048": "RSA", "ECDSA-P256": "ECDSA"}
ACCENT, GREY = "#1F2A7A", "#9EA1AA"


def plain_number(value, _pos):
    return f"{value:g}"


def charts(df):
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    machines = list(dict.fromkeys(df.machine))
    for group in GROUP_TITLES:
        gdf = df[df.group == group]
        algos = ALGOS[group]
        fig, axes = plt.subplots(1, len(machines), figsize=(7.4, 2.5), squeeze=False)
        for ax, machine in zip(axes[0], machines):
            data = [gdf[(gdf.machine == machine) & (gdf.algorithm == a)].ms for a in algos]
            ax.boxplot(data, tick_labels=[SHORT.get(a, a) for a in algos], widths=0.55, patch_artist=True,
                       boxprops={"facecolor": "#DDE0EE", "edgecolor": ACCENT, "linewidth": 0.8},
                       medianprops={"color": ACCENT, "linewidth": 1.6},
                       whiskerprops={"color": ACCENT, "linewidth": 0.8}, capprops={"color": ACCENT, "linewidth": 0.8},
                       flierprops={"marker": "o", "markersize": 3, "markerfacecolor": GREY, "markeredgecolor": GREY})
            ax.set_title(SETUP_NAMES.get(machine, machine), fontsize=9.5)
            ax.grid(axis="y", color="#E6E6E6", linewidth=0.6)
            ax.set_xticks(range(1, len(algos) + 1), [SHORT.get(a, a) for a in algos], fontsize=7.5)
            ax.tick_params(axis="x", length=0)
            ax.set_axisbelow(True)
            if group == "symmetric":
                ax.set_yscale("log")
                ax.yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
                ax.yaxis.set_minor_formatter(NullFormatter())
                ax.set_ylim(top=max(s.max() for s in data) * 1.4)
            else:
                ax.set_ylim(bottom=0)  # linear axes start at zero so gaps are not exaggerated
            ax.yaxis.set_major_formatter(FuncFormatter(plain_number))
        axes[0][0].set_ylabel("time (ms)")
        fig.tight_layout(w_pad=1.2)
        fig.savefig(OUT / f"time_{group}.png", dpi=220)
        plt.close(fig)

    sizes = DATA / "sizes.csv"
    if sizes.exists():
        sdf = pd.read_csv(sizes)
        sig = sdf[sdf.metric == "signature"]
        fig, ax = plt.subplots(figsize=(4.4, 2.4))
        bars = ax.bar(sig.algorithm, sig.bytes, width=0.55, color=[ACCENT if f else GREY for f in sig.fits_one_ble_packet])
        ax.bar_label(bars, labels=[f"{b} B" for b in sig.bytes], padding=2, fontsize=8.5)
        ax.axhline(244, ls="--", color="black", linewidth=1)
        ax.text(2.3, 232, "one BLE packet: 244 B", ha="right", va="top", fontsize=8.5)
        ax.set_ylim(0, 290)
        ax.set_ylabel("signature size (bytes)")
        fig.tight_layout()
        fig.savefig(OUT / "size_signature.png", dpi=220)
        plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    files = sorted(DATA.glob("time_*.csv"), key=lambda p: ("no-crypto" in p.name, p.name))
    df = pd.concat([pd.read_csv(p) for p in files], ignore_index=True)
    report = analyse(df)
    (OUT / "stats.md").write_text(report)
    charts(df)
    print(report)


if __name__ == "__main__":
    main()
