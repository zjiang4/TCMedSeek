# -*- coding: utf-8 -*-
"""TCMedSeek manuscript figures. Generates 300-DPI PNGs into ./figures/."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

# Okabe-Ito colorblind-safe palette
BLUE, ORANGE, GREEN, VERM = "#0072B2", "#E69F00", "#009E73", "#D55E00"
SKY, PURPLE, GRAY = "#56B4E9", "#CC79A7", "#666666"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.linewidth": 0.8, "savefig.dpi": 300, "figure.dpi": 300,
})


def box(ax, x, y, w, h, title, sub, fc, ec, title_fs=10, sub_fs=8.2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                       linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=3)
    ax.add_patch(p)
    if sub:
        ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color="#1a1a1a", zorder=4)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
                fontsize=sub_fs, color="#333333", zorder=4, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color="#1a1a1a", zorder=4, linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, color="#444444", lw=1.6, style="-|>", ls="-", rad=0.0, zorder=2):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                        linewidth=lw, color=color, linestyle=ls, zorder=zorder,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)


# ---------------------------------------------------------------- Fig 1
def fig1_workflow():
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 63); ax.axis("off")

    # main cycle boxes
    box(ax, 7, 50, 24, 10, "Training corpus $D_t$",
        "135,797 samples, 87% authoritative\nprovenance to volume and line",
        "#cfe3f5", BLUE)
    box(ax, 38, 50, 24, 10, "Single-stage LoRA SFT",
        "Qwen3.6-35B-A3B, 1 epoch\nno CPT, no RL, no RAG",
        "#fdf0d5", ORANGE)
    box(ax, 69, 50, 26, 10, "Full-coverage evaluation",
        "frozen slice, MTCMB 11 subsets\nprotocol levels L0 / L1 / L2",
        "#d6efe4", GREEN)
    box(ax, 69, 36, 26, 8, "Closed-set error extraction",
        "multiple-choice and multi-label items", "#eff3f6", GRAY)
    box(ax, 69, 20, 26, 8, "Automated attribution",
        "knowledge-skeleton match", "#eff3f6", GRAY)

    # remediation branches (bottom row)
    box(ax, 6, 4, 26, 10, "Knowledge gap (68)",
        "add new corpus material\nwith provenance", "#d6efe4", GREEN, 9.2, 7.8)
    box(ax, 44, 4, 28, 10, "Misdiscriminated (454)",
        "contrastive cards\nnaming the distractor", "#d6efe4", GREEN, 9.2, 7.8)
    box(ax, 76, 4, 20, 10, "Reference fault (143)",
        "authority arbitration,\nscore-independent evidence", "#fbe3e0", VERM, 9.2, 7.8)

    # gate
    box(ax, 8, 22, 24, 10, "Decontamination gate",
        "six channels + independent\nre-implementation, both zero",
        "#e4d9ee", PURPLE)

    # main-cycle arrows
    arrow(ax, 31.5, 55, 37.5, 55)
    arrow(ax, 62.5, 55, 68.5, 55)
    arrow(ax, 82, 49.7, 82, 44.5)
    arrow(ax, 82, 35.7, 82, 28.5)
    # attribution fan to three branches
    arrow(ax, 74, 19.7, 20, 14.5, rad=0.0, lw=1.3)
    arrow(ax, 79, 19.7, 58, 14.5, lw=1.3)
    arrow(ax, 85, 19.7, 86, 14.5, lw=1.3)
    # return bus: drops from branches, trunk along bottom, up far-left into gate
    for gx in (19, 58, 86):
        arrow(ax, gx, 3.7, gx, 1.6, style="-", lw=1.3, color=GRAY)
    arrow(ax, 86, 1.6, 3, 1.6, style="-", lw=1.3, color=GRAY)
    arrow(ax, 3, 1.6, 3, 27, style="-", lw=1.3, color=GRAY)
    arrow(ax, 3, 27, 7.5, 27, lw=1.3, color=GRAY)
    # gate -> corpus
    arrow(ax, 20, 32.3, 20, 49.5, color=PURPLE)

    # loop badge
    ax.add_patch(Circle((52, 40), 6.2, fill=True, facecolor="#f5f5f5",
                        edgecolor=GRAY, linewidth=1.0, linestyle="--", zorder=1))
    ax.text(52, 40, "33 iterations", ha="center", va="center",
            fontsize=9.5, color="#333333", zorder=2)

    fig.savefig(os.path.join(OUT, "fig1_workflow.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Fig 2
def fig2_corpus():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.4),
                                 gridspec_kw={"width_ratios": [1.05, 1]})
    src = [("Textbooks (35 vols)", 55.67), ("Exercise sets (18 vols)", 18.15),
           ("Pharmacopoeia 2020", 13.02), ("Public cases (TCM-SD)", 7.93),
           ("Hand-written / rewrites", 1.70), ("National std terms", 1.45),
           ("General alignment", 0.76), ("Classical texts", 0.67),
           ("Constructed format", 0.53), ("Undetermined", 0.12)]
    src = src[::-1]
    labels = [s[0] for s in src]; vals = [s[1] for s in src]
    cols = [GRAY if v < 5 else (VERM if "Undetermined" in l else BLUE) for l, v in src]
    a1.barh(labels, vals, color=cols, edgecolor="white", height=0.68)
    for i, v in enumerate(vals):
        a1.text(v + 0.8, i, f"{v:.2f}%", va="center", fontsize=7.6, color="#333333")
    a1.set_xlim(0, 63); a1.set_xlabel("Share of training corpus (%)")
    a1.set_title("(a) Corpus composition (n = 135,797)", fontsize=9.5, loc="left")
    a1.tick_params(labelsize=7.8); a1.spines[["top", "right"]].set_visible(False)

    routes = [("Declared at build time", 71520), ("Retro-traced", 59616),
              ("Declared, no upstream", 3342), ("By construction", 716),
              ("Declared (trust_src)", 437), ("Undetermined", 166)][::-1]
    rl = [r[0] for r in routes]; rv = [r[1] for r in routes]
    cols2 = [VERM if "Undetermined" in x else SKY for x in rl]
    a2.barh(rl, rv, color=cols2, edgecolor="white", height=0.68)
    a2.set_xscale("log"); a2.set_xlim(60, 4.5e5)
    for i, v in enumerate(rv):
        a2.text(v * 1.18, i, f"{v:,}", va="center", fontsize=7.6, color="#333333")
    a2.set_xlabel("Samples (log scale)")
    a2.set_title("(b) Provenance adjudication routes", fontsize=9.5, loc="left")
    a2.tick_params(labelsize=7.8); a2.spines[["top", "right"]].set_visible(False)
    a2.annotate("29.7% undetermined before\ntracing, 0.12% after",
                xy=(166, 0), xytext=(2500, 0.75), fontsize=7.6, color=VERM,
                arrowprops=dict(arrowstyle="->", color=VERM, lw=0.9))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_corpus.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Fig 3
def fig3_bandwidth():
    data = [  # name, L0, L1, L2, bandwidth, highlight
        ("HuatuoGPT-o1-8B", 9.73, 17.66, 26.67, 16.93, VERM),
        ("HuatuoGPT2-7B", 12.94, 19.08, 19.87, 6.93, None),
        ("HuatuoGPT2-34B", 27.22, 29.39, 33.48, 6.26, None),
        ("Baichuan-M1-14B", 51.18, 53.57, 60.42, 9.24, None),
        ("Sunsimiao-7B", 52.08, 55.62, 55.68, 3.60, None),
        ("BianCang-7B", 54.34, 59.44, 60.24, 5.91, None),
        ("ShizhenGPT-7B", 56.18, 56.18, 57.29, 1.11, None),
        ("Fu-TCM-27B", 60.07, 60.07, 60.21, 0.14, None),
        ("Xinghe1.2-9B", 62.21, 62.50, 63.38, 1.17, None),
        ("Untrained base", 62.91, 67.85, 68.53, 5.62, ORANGE),
        ("ShizhenGPT-32B", 64.80, 64.80, 66.04, 1.24, None),
        ("BianCang-14B", 64.88, 64.88, 65.05, 0.17, None),
        ("TCMedSeek", 73.97, 73.97, 74.54, 0.57, BLUE),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ys = range(len(data))
    for y, (name, l0, l1, l2, bw, hl) in zip(ys, data):
        c = hl or GRAY
        ax.plot([l0, l2], [y, y], color=c, lw=3.2, alpha=0.35, solid_capstyle="round", zorder=2)
        ax.scatter([l0], [y], s=30, c=c, marker="o", zorder=3)
        ax.scatter([l1], [y], s=24, c=c, marker="^", zorder=4)
        ax.scatter([l2], [y], s=30, c=c, marker="s", zorder=3)
        ax.text(75.4, y, f"+{bw:.2f}", va="center", fontsize=7.8,
                color=c, fontweight="bold" if hl else "normal")
    ax.set_yticks(list(ys)); ax.set_yticklabels([d[0] for d in data], fontsize=8.4)
    ax.set_xlim(0, 80); ax.set_ylim(-0.7, len(data) - 0.3)
    ax.set_xlabel("10-subset average score")
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=GRAY, markersize=6, label="L0 (no extraction)"),
               Line2D([0], [0], marker="^", color="none", markerfacecolor=GRAY, markersize=6, label="L1 (first letter)"),
               Line2D([0], [0], marker="s", color="none", markerfacecolor=GRAY, markersize=6, label="L2 (full extractor)"),
               Line2D([0], [0], color=GRAY, lw=3.2, alpha=0.35, label="protocol bandwidth (L2 to L0)")]
    ax.legend(handles=handles, loc="lower left", fontsize=7.6, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(75.4, len(data) - 0.55, "bandwidth", fontsize=7.8, color="#333333", style="italic")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3_bandwidth.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Fig 4
def fig4_margins():
    data = [("MSDD", 14.50, "win"), ("CHGD", 7.79, "win"), ("Diagnosis", 6.27, "win"),
            ("FRD", 6.21, "win"), ("SE-B", 4.00, "win"), ("ED-A", 2.34, "win"),
            ("TCMeEE", 0.78, "tie"), ("ED-B", 0.46, "tie"),
            ("PR", -1.23, "tie"), ("LitData", -5.40, "loss")]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ys = range(len(data))
    ax.axvspan(-1.0, 1.0, color="#000000", alpha=0.07, zorder=1)
    ax.axvline(0, color="#888888", lw=0.9)
    cmap = {"win": BLUE, "tie": "#999999", "loss": VERM}
    for y, (name, m, v) in zip(ys, data):
        ax.barh(y, m, left=0, height=0.62, color=cmap[v], zorder=3,
                edgecolor="white")
        off = 0.35 if m >= 0 else -0.35
        ax.text(m + off, y, f"{m:+.2f}", va="center",
                ha="left" if m >= 0 else "right", fontsize=8, color=cmap[v])
    ax.set_yticks(list(ys)); ax.set_yticklabels([d[0] for d in data], fontsize=8.6)
    ax.invert_yaxis()
    ax.set_xlim(-8, 17.5)
    ax.set_xlabel("Margin of TCMedSeek v7.9 over strongest external model (L2)")
    ax.text(0.15, 9.55, "within noise band", fontsize=7.4, color="#555555", rotation=90, va="bottom")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4_margins.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Fig S1
def figS1_versions():
    ver = ["v4.2", "v5.0", "v5.5", "v5.33", "v6.4", "v7.3", "v7.4-Q", "v7.7", "v7.8e", "v7.9"]
    rows = [131753, 124231, 110415, 116452, 133849, 138386, 138264, 135622, 135864, 135797]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(ver, rows, "-o", color=BLUE, lw=1.6, ms=4.5, mfc="white", mew=1.4)
    for x, y in zip(ver, rows):
        ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=7.2, color="#333333")
    ax.annotate("leak-purge minimum", xy=("v5.5", 110415), xytext=(1.05, 112500),
                fontsize=7.6, color=VERM,
                arrowprops=dict(arrowstyle="->", color=VERM, lw=0.9))
    ax.annotate("delivered", xy=("v7.9", 135797), xytext=(8.15, 130800),
                fontsize=7.6, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9))
    ax.set_ylim(106000, 142000); ax.set_ylabel("Training-set rows")
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figS1_versions.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig1_workflow(); fig2_corpus(); fig3_bandwidth(); fig4_margins()
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
