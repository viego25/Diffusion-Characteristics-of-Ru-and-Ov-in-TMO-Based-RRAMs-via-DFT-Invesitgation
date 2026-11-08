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

kB = 8.617333262e-5       # eV/K
L = 1e-7                  # cm (1 nm)

T = np.linspace(300, 700, 401)

# ==========================================================
# Diffusion prefactors (cm²/s)
# ==========================================================

D0_ZrO2 = 2.34e-2
D0_HfO2 = 0.082

# ==========================================================
# Activation energies (eV)
# ==========================================================

Ea_ZrO2_neutral = 1.27
Ea_ZrO2_plus2   = 0.29

Ea_HfO2_neutral = 1.52
Ea_HfO2_plus2   = 0.30

# ==========================================================
# Functions
# ==========================================================

def diffusion(D0, Ea):
    return D0 * np.exp(-Ea / (kB * T))

def diffusion_time(D):
    return L**2 / (2 * D)

# ==========================================================
# Calculate diffusion times
# ==========================================================

tzr_n  = diffusion_time(diffusion(D0_ZrO2, Ea_ZrO2_neutral))
tzr_p2 = diffusion_time(diffusion(D0_ZrO2, Ea_ZrO2_plus2))

thf_n  = diffusion_time(diffusion(D0_HfO2, Ea_HfO2_neutral))
thf_p2 = diffusion_time(diffusion(D0_HfO2, Ea_HfO2_plus2))

# ==========================================================
# Print diffusion times at 300 K and 700 K
# ==========================================================

temps = [300, 700]

print("\n================ Diffusion Times ================\n")

for temp in temps:
    idx = np.argmin(np.abs(T - temp))

    print(f"T = {T[idx]:.0f} K")
    print(f"  ZrO2 OV^0   : {tzr_n[idx]:.6e} s")
    print(f"  ZrO2 OV^2+  : {tzr_p2[idx]:.6e} s")
    print(f"  HfO2 OV^0   : {thf_n[idx]:.6e} s")
    print(f"  HfO2 OV^2+  : {thf_p2[idx]:.6e} s")
    print("-" * 45)

# ==========================================================
# Colors
# ==========================================================

zr_color = "#0B5FA5"   # Deep sapphire blue
hf_color = "#A2142F"   # Deep crimson red

# ==========================================================
# Figure
# ==========================================================

fig, ax = plt.subplots(figsize=(8.2, 6.2), dpi=600)

# --------------------- ZrO2 ---------------------

ax.semilogy(
    T,
    tzr_n,
    color=zr_color,
    linewidth=3.4,
    solid_capstyle='round',
    label='ZrO$_2$ OV$^{0}$'
)

ax.semilogy(
    T,
    tzr_p2,
    color=zr_color,
    linewidth=3.4,
    linestyle='--',
    solid_capstyle='round',
    label='ZrO$_2$ OV$^{2+}$'
)

# --------------------- HfO2 ---------------------

ax.semilogy(
    T,
    thf_n,
    color=hf_color,
    linewidth=3.4,
    solid_capstyle='round',
    label='HfO$_2$ OV$^{0}$'
)

ax.semilogy(
    T,
    thf_p2,
    color=hf_color,
    linewidth=3.4,
    linestyle='--',
    solid_capstyle='round',
    label='HfO$_2$ OV$^{2+}$'
)

# ==========================================================
# Formatting
# ==========================================================

ax.set_xlim(300, 700)

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

# Minor ticks
ax.minorticks_on()

# Tick formatting
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

# Make tick labels bold
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
    "Diffusion_Time.png",
    dpi=600,
    bbox_inches='tight'
)

plt.savefig(
    "Diffusion_Time.pdf",
    bbox_inches='tight'
)

plt.show()