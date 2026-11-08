import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Configure matplotlib to use Times New Roman for all elements
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Liberation Serif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

# Raw dataset coordinates loaded from .dat files
dat_files = {
    "Path A": "A.dat",
    "Path B": "B.dat",
    "Path C": "C.dat",
    "Path D": "D.dat",
    "Path E": "E.dat",
    "Path F": "F.dat",
}

data_paths = {name: np.loadtxt(fname).tolist() for name, fname in dat_files.items()}

# Canvas initialization
fig, ax = plt.subplots(figsize=(6.5, 5), dpi=300)

colors = [
    '#D81B60',  # Crimson Rose
    '#1E88E5',  # Royal Blue
    '#00897B',  # Teal
    '#F57C00',  # Deep Orange
    '#6A1B9A',  # Royal Purple
    '#5D4037'   # Dark Cocoa Brown
]

# Generate paths
for i, path_name in enumerate(sorted(data_paths.keys())):

    pts = np.array(data_paths[path_name])

    x = pts[:, 0]
    y = pts[:, 1]

    # Sort coordinate points
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    y = y[sort_idx]

    # Cubic spline
    x_smooth = np.linspace(x.min(), x.max(), 300)
    cs = CubicSpline(x, y)
    y_smooth = cs(x_smooth)

    # Plot smooth curve
    ax.plot(
        x_smooth,
        y_smooth,
        label=path_name,
        color=colors[i],
        linewidth=2.0,
        linestyle='--',
        zorder=2
    )

    # Plot markers
    ax.scatter(
        x,
        y,
        color=colors[i],
        marker='o',
        s=35,
        edgecolors='none',
        clip_on=False,
        zorder=10
    )

# ============================================================
# Border ABOVE curves and markers
# ============================================================

for spine in ax.spines.values():
    spine.set_linewidth(1.5)
    spine.set_zorder(100)

ax.set_axisbelow(False)

# Axis labels
ax.set_xlabel(
    'Reaction Coordinate',
    fontsize=22,
    labelpad=8,
    fontweight='bold'
)

ax.set_ylabel(
    'Energy Landscape (eV)',
    fontsize=22,
    labelpad=8,
    fontweight='bold'
)

# Limits
ax.set_xlim(0, 1)
ax.set_ylim(-0.15, 1.4)

# Ticks
ax.tick_params(
    axis='both',
    which='both',
    direction='in',
    top=True,
    right=True,
    labelsize=18,
    width=1.5,
    length=6
)

# Legend
ax.legend(
    loc='upper left',
    frameon=False,
    handlelength=1.5,
    prop={
        'family': 'Times New Roman',
        'weight': 'bold',
        'size': 14
    }
)

plt.tight_layout()

plt.savefig(
    'neb_thick_border.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()