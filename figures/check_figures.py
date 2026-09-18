# -*- coding: utf-8 -*-
"""Validate figures geometrically: every text/legend artist must sit inside the
canvas; overlapping text inside different boxes is not checked (single source
of truth is the layout code)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import make_figures as MF

plt.close = lambda *a, **k: None  # keep figures open for inspection

MF.fig1_workflow(); MF.fig2_corpus(); MF.fig3_bandwidth(); MF.fig4_margins()

problems = 0
for num in plt.get_fignums():
    fig = plt.figure(num)
    fig.canvas.draw()
    fw, fh = fig.canvas.get_width_height()
    renderer = fig.canvas.get_renderer()
    name = {1: "fig1", 2: "fig2", 3: "fig3", 4: "fig4"}.get(num, f"fig{num}")
    for ax in fig.axes:
        for t in ax.texts:
            bb = t.get_window_extent(renderer=renderer)
            if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > fw + 2 or bb.y1 > fh + 2:
                problems += 1
                print(f"[OUT] {name}: text '{t.get_text()[:40]}' "
                      f"bb=({bb.x0:.0f},{bb.y0:.0f})-({bb.x1:.0f},{bb.y1:.0f}) "
                      f"canvas={fw}x{fh}")
        leg = ax.get_legend()
        if leg is not None:
            bb = leg.get_window_extent(renderer=renderer)
            if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > fw or bb.y1 > fh:
                problems += 1
                print(f"[OUT] {name}: legend exceeds canvas")
    print(f"{name}: canvas {fw}x{fh}, texts checked={sum(len(a.texts) for a in fig.axes)}")

print("RESULT:", "PASS" if problems == 0 else f"{problems} problem(s)")
