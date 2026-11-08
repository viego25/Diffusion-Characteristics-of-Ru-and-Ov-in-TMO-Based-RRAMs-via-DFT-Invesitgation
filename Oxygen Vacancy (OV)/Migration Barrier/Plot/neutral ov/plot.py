import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ============================================================
# Times New Roman
# ============================================================

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Liberation Serif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

# ============================================================
# Data files
# ============================================================

dat_files = {
    "Path A": "A.dat",
    "Path B": "B.dat",
    "Path C": "C.dat",
    "Path D": "D.dat",
    "Path E": "E.dat",
    "Path F": "F.dat",
}

colors = [
    '#D81B60',  # Crimson Rose
    '#1E88E5',  # Royal Blue
    '#00897B',  # Teal
    '#F57C00',  # Deep Orange
    '#6A1B9A',  # Royal Purple
    '#5D4037'   # Dark Cocoa Brown
]

# ============================================================
# Figure (same style as reference)
# ============================================================

fig, ax = plt.subplots(figsize=(6.5, 5), dpi=300)

# ============================================================
# Find global y-range
# ============================================================

ymin = np.inf
ymax = -np.inf

# ============================================================
# Plot
# ============================================================

for i, (label, filename) in enumerate(dat_files.items()):

    data = np.loadtxt(filename)

    x = data[:, 0]
    y = data[:, 1]

    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]

    spline = CubicSpline(x, y)

    xx = np.linspace(x.min(), x.max(), 500)
    yy = spline(xx)

    ymin = min(ymin, yy.min())
    ymax = max(ymax, yy.max())

    # Smooth curve
    ax.plot(xx,
            yy,
            color=colors[i],
            linewidth=2.5,
            linestyle='-',
            label=label,
            zorder=2)

    # Original data points
    ax.scatter(x,
               y,
               s=45,
               color=colors[i],
               edgecolors='none',
               clip_on=False,
               zorder=10)

# ============================================================
# Automatic y-limit
# ============================================================

pad = 0.06 * (ymax - ymin)

ax.set_xlim(0, 1)
ax.set_ylim(ymin - pad, ymax + pad)

# ============================================================
# Axis Labels
# ============================================================

ax.set_xlabel("Reaction Coordinate",
              fontsize=22,
              fontweight='bold',
              labelpad=8)

ax.set_ylabel("Energy Landscape (eV)",
              fontsize=22,
              fontweight='bold',
              labelpad=8)

# ============================================================
# Tick Formatting
# ============================================================

ax.tick_params(axis='both',
               which='both',
               direction='in',
               top=True,
               right=True,
               width=1.5,
               length=6,
               labelsize=18)

# ============================================================
# Thick Border
# ============================================================

for spine in ax.spines.values():
    spine.set_linewidth(1.5)
    spine.set_zorder(100)

ax.set_axisbelow(False)

# ============================================================
# Legend
# ============================================================

legend = ax.legend(
    loc='upper left',
    frameon=False,
    handlelength=1.5,
    prop={
        'family': 'Times New Roman',
        'weight': 'bold',
        'size': 14
    }
)

# ============================================================
# Layout
# ============================================================

plt.tight_layout()

# ============================================================
# Save Figure
# ============================================================

plt.savefig("energy_landscape.png",
            dpi=300,
            bbox_inches='tight')

plt.show()