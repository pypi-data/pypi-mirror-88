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
from mpl_toolkits.mplot3d import Axes3D


# documentation for all functions and commands:
def docs():
    print(
        "[1] ssap.info()\n"
        "[2] ssap.docs()\n"
        "[3] ssap.bsfcmap(speed,torque,bsfc,title,level)"
        "[4] ssap.dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,title)"
        
        "--------------------------------------------------------------------"
        "[Details]:"
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


# bsfcmap | 20.dec.09
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

# dutycycle | 20.dec.10
def dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,bubblesize,title):
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

    ax.scatter(xpos, ypos, s=hist*bubblesize, alpha=0.5)
    ax.set_xlabel('Engine speed (rpm)')
    ax.set_ylabel('Torque (N.m)')
    ax.set_title(title)
    plt.show()

# dutycycle3d plot | 20.dec.14
def dutycycle3d(speed, torque, colnum, title):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    # %matplotlib notebook

    # define inputs for this function.
    x = speed
    y = torque
    bins = colnum
    title = title

    # basic function.
    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=bins)

    hist1 = hist_temp.T

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Construct arrays for the anchor positions of all the bars. add_subplot(111) - standard format for 3d plotting. x,y,z axis
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos1 = 0

    # Construct arrays with bar dimension
    dx = int(2 / 3 * (max(x) - min(x)) / (bins))
    dy = int(2 / 3 * (max(y) - min(y)) / (bins))

    dz1 = hist1.ravel()
    # dz2 = hist2.ravel()

    ax.bar3d(xpos, ypos, zpos1, dx, dy, dz1, zsort='average', color='skyblue', edgecolor='black', linewidth=0.3,
             alpha=0.4)
    # ax.bar3d(xpos, ypos, zpos1, dx, dy, dz2, zsort='average', color='orange',alpha=0.5)
    ax.set_xlabel('Engine Speed(rpm)')
    ax.set_ylabel('Torque(N.m)')
    ax.set_title(title)
    plt.show()



