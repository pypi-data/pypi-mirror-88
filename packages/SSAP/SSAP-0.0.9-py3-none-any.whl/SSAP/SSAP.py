# Author:tony
# Create time:2020.12.09
# The software is build 4 SSAP POC testing.

# %$ → Next plan: GUI, pop up web visualization, engineering charts.

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# documentation for all functions and commands:
def docs():
    print(
        "[1] ssap.info() - SSAP python package description;\n"
        "[2] ssap.docs() - All function modules and commands in SSAP package;\n"
        "[3] ssap.bsfcmap(speed,torque,bsfc,title,level) - ICE bsfcmap chart\n"
        "\t ● speed:engine speed\n"
        "\t ● torque:engine torque\n"
        "\t ● bsfc:engine bfsc\n"
        "\t ● title:create a name for your bsfcmap\n"
        "\t ● level:define bsfcmap level array\n"
    )

# basic introduction
def info():
    print('Welcome to SSAP! SSAP→[Self Service Analytics Platform]. There are different analytics function modules to '
          'support you complete different data analytics scenarios. Please enjoy! Any question or support needed, '
          'please raise in Big Data Community(BDC).')


# bsfcmap
def bsfcmap(speed, torque, bsfc, title, level):
    x = np.array(speed)
    y = np.array(torque)
    z = np.array(bsfc)
    level = level
    title = title

    xi = np.linspace(min(x), max(x), 1000)
    yi = np.linspace(min(y), max(y), 1000)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # method: nearest / linear / cubic
    plt.figure(figsize=(12, 8))
    C = plt.contour(X, Y, Z, level, colors='black', alpha=0.5)
    plt.contourf(X, Y, Z, level, alpha=.75, cmap='plasma')
    plt.colorbar()
    plt.clabel(C, inline=True, fontsize=10, colors='black')
    plt.xlabel('Engine_Speed(rpm)')
    plt.ylabel('Engine_Torque(N.m)')
    plt.title(title)
    plt.show()
