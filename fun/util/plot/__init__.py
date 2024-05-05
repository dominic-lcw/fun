import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# -------------------------------------------------
# Set Default Color Code
# Reference: 
# https://www.color-hex.com/color-palette/1044555
# -------------------------------------------------

# Color blind safe
# default_color = [
#     "#edbd00", "#ff5e00", "#7487ff", "#8abbff", "#1dd2d3",
# ]

# Beauty and The Beast
default_color = [
    "#0b0269", "#66b2b2", "#b8a916", "#9ca5aa", "#ffe700",
]

mpl.rcParams['axes.prop_cycle'] = mpl.cycler(
    color = default_color
)

