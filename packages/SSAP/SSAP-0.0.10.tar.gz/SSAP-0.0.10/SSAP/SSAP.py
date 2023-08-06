# ***********************************************************************************
# Author:tony qin
# Create time:2020.12.08
# The software is build 4 SSAP poc testing.
# Vision of (SSAP)Self Service analytics platform is to promote every users to grasp the self-service analytics capability.

# %$ → [Next plan: GUI, pop up web visualization, eng charts.]
# duty cycle, normality test report,

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
        "\t ● title:create a name for your chart\n"
        "\t ● level: bsfcmap boundary level matrix, define graininess for your map.\n"
        
        "[4] ssap.dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,title) - ICE duty cycle chart\n"
        "\t ● speed:engine speed\n"
        "\t ● torque:engine torque\n"
        "\t ● x1:speed start point\n"
        "\t ● x2:speed end point\n"
        "\t ● stepx:speed gap distance\n"
        "\t ● y1:torque start point\n"
        "\t ● y2:torque end point\n"
        "\t ● stepy:torque gap distance\n"
        "\t ● title:create a name for your chart\n"
    )


# links
def link():
    print(
        "[1] Travel request | https://connect.citsgbt.com/online/login\n"
        "[2] CBP(Leave|Product access apply) | https://cbp.cummins.com.cn/\n"
        "[3] CIP | http://digital.cummins.com.cn/cip.ui/login.jsp#\n"
        "[4] BDC | https://www.yammer.com/cummins.com/#/threads/inGroup?type=in_group&feedId=17547968512&view=all\n"
        "[5] pypi step1 | python setup.py sdist bdist_wheel\n"
        "[6] pypi step2 | twine upload dist/*\n"
    )


# basic introduction
def info():
    print('Welcome to SSAP! SSAP→[Self Service Analytics Platform]. There are different analytics function modules to '
          'support you complete different data analytics scenarios. Please enjoy! Any question or support needed, '
          'please raise in Big Data Community(BDC).')

# bsfcmap 2020.12.09
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

# dutycycle 2020.12.10
def dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,title):
    x = speed
    y = torque

    xedges = [*range(x1,x2,stepx)]
    yedges = [*range(y1,y2,stepy)]

    hist_temp, xedges, yedges = np.histogram2d(x, y, bins = (xedges,yedges))
    hist = hist_temp.T
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()

    fig, ax = plt.subplots(figsize=(14,8))

    ax.set_xticks(xedges , minor=False)
    ax.set_yticks(yedges , minor=False)

    ax.grid(which='both',color='grey',linestyle='--',alpha=0.6)

    ax.scatter(xpos, ypos, s=hist*1800, alpha=0.5)
    ax.set_xlabel('Engine speed (rpm)')
    ax.set_ylabel('Torque (N.m)')
    ax.set_title(title)
    plt.show()


