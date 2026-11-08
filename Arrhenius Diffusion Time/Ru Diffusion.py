import numpy as np
import matplotlib.pyplot as plt


plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
    "font.size": 16,
    "font.weight": "bold",
    "axes.labelweight": "bold",
    "axes.linewidth": 1.8,
    "axes.labelsize": 20,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 14,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 7,
    "ytick.major.size": 7,
    "xtick.minor.size": 4,
    "ytick.minor.size": 4,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.minor.width": 1.2,
    "ytick.minor.width": 1.2,
})

# ==========================================================
# Constants
# ==========================================================

kB = 8.617333262e-5      # eV/K
L  = 1e-7                # cm (1 nm)

T = np.linspace(300, 700, 401)

# ==========================================================
# Diffusion Prefactors (cm²/s)
# ==========================================================

D0_ZrO2 = 2.34e-2
D0_HfO2 = 0.082

# ==========================================================
# Migration Barriers (eV)
# ==========================================================

Ea_ZrO2 = 0.26
Ea_HfO2 = 0.20

# ==========================================================
# Functions
# ==========================================================

def diffusion(D0, Ea):
    return D0 * np.exp(-Ea / (kB * T))

def diffusion_time(D):
    return L**2 / (2 * D)

# ==========================================================
# Calculate Diffusion Times
# ==========================================================

tzr = diffusion_time(diffusion(D0_ZrO2, Ea_ZrO2))
thf = diffusion_time(diffusion(D0_HfO2, Ea_HfO2))

# ==========================================================
# Color (Publication Quality)
# ==========================================================

ru_color = '#6A5ACD'      # Royal orange

# ==========================================================
# Figure
# ==========================================================

fig, ax = plt.subplots(figsize=(8.2, 6.2), dpi=600)

# --------------------- HfO2 ---------------------

ax.semilogy(
    T,
    thf,
    color=ru_color,
    linewidth=3.4,
    linestyle='-',
    solid_capstyle='round',
    label='Ru$_i$ in HfO$_2$'
)

# --------------------- ZrO2 ---------------------

ax.semilogy(
    T,
    tzr,
    color=ru_color,
    linewidth=3.4,
    linestyle='--',
    dash_capstyle='round',
    label='Ru$_i$ in ZrO$_2$'
)

# ==========================================================
# ==========================================================
# Formatting
# ==========================================================

ax.set_xlim(300, 700)

# Publication-quality y-axis limits
ax.set_ylim(1e-13, 1e-7)

# Publication-quality log ticks
ax.set_yticks([1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-8, 1e-7])

ax.set_xlabel(
    "Temperature (K)",
    fontsize=26,
    fontweight='bold',
    fontname='Times New Roman'
)

ax.set_ylabel(
    "Diffusion Time (s)",
    fontsize=26,
    fontweight='bold',
    fontname='Times New Roman'
)

ax.minorticks_on()

ax.tick_params(
    which='major',
    direction='in',
    top=True,
    right=True,
    length=7,
    width=1.5
)

ax.tick_params(
    which='minor',
    direction='in',
    top=True,
    right=True,
    length=4,
    width=1.2
)

# Bold tick labels
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
    tick.set_fontname('Times New Roman')

for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')
    tick.set_fontname('Times New Roman')

# Thick border
for spine in ax.spines.values():
    spine.set_linewidth(1.8)

# No grid
ax.grid(False)

# Legend
leg = ax.legend(
    frameon=False,
    loc='best',
    handlelength=3
)

for text in leg.get_texts():
    text.set_fontname("Times New Roman")
    text.set_fontweight("bold")

# Bold tick labels
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
    tick.set_fontname('Times New Roman')

for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')
    tick.set_fontname('Times New Roman')

# Thick border
for spine in ax.spines.values():
    spine.set_linewidth(1.8)

# No grid
ax.grid(False)

# Legend
leg = ax.legend(
    frameon=False,
    loc='best',
    handlelength=3
)

for text in leg.get_texts():
    text.set_fontname("Times New Roman")
    text.set_fontweight("bold")

plt.tight_layout()

# ==========================================================
# Save Figure
# ==========================================================

plt.savefig(
    "Ru_Interstitial_Diffusion_Time.png",
    dpi=600,
    bbox_inches='tight'
)

plt.savefig(
    "Ru_Interstitial_Diffusion_Time.pdf",
    bbox_inches='tight'
)

plt.show()