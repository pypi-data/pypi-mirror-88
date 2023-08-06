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


# basic introduction
def info():
    print('Welcome to SSAP! SSAP→[Self Service Analytics Platform]. There are different analytics function modules to '
          'support you complete different data analytics scenarios. Please enjoy! Any question or support needed, '
          'please raise in Big Data Community(BDC).')


# documentation for all functions and commands:
def docs():

    # print abstract:
    print(
        "[1] ssap.info()\n"
        "[2] ssap.docs()\n"
        "[3] ssap.bsfcmap(speed,torque,bsfc,title,level)\n"
        "[4] ssap.dutycycle(speed,torque,x1,x2,stepx,xlabel,y1,y2,stepy,ylabel,bubblesize,title)\n"
        "[5] ssap.dutycycle3d(speed,torque,3dbar_num,title)\n"
        "[6] ssap.boxplot01(parameter column,label,title)\n"
        "[7] ssap.boxplot02(dataframe,title)\n"
        "[8] ssap.boxplot03(df, category_x_name, value_y_name, title)\n"
        "[9] ssap.pdsclean(df)\n"
        "[10] ssap.cmd()\n"
    )
    # explain details:
    # print(
    #     "--------------------------------------------------------------------\n"
    #     "[Details]:\n"
    #     "[1] ssap.info() - SSAP python package description;\n"
    #
    #     "[2] ssap.docs() - All function modules and commands in SSAP package;\n"
    #
    #     "[3] ssap.bsfcmap(speed,torque,bsfc,title,level) - ICE bsfcmap chart\n"
    #     "\t ● speed:engine speed\n"
    #     "\t ● torque:engine torque\n"
    #     "\t ● bsfc:engine bfsc\n"
    #     "\t ● title:create a name for your chart\n"
    #     "\t ● level: bsfcmap boundary level matrix, define graininess for your map.\n"
    #
    #     "[4] ssap.dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,title) - ICE duty cycle chart\n"
    #     "\t ● speed:engine speed\n"
    #     "\t ● torque:engine torque\n"
    #     "\t ● x1:speed start point\n"
    #     "\t ● x2:speed end point\n"
    #     "\t ● stepx:speed gap distance\n"
    #     "\t ● y1:torque start point\n"
    #     "\t ● y2:torque end point\n"
    #     "\t ● stepy:torque gap distance\n"
    #     "\t ● title:create a name for your chart\n"
    #
    #     "[5] ..."
    # )


# ※※other common python commands:
def cmd():
    print(
        "[1] pd.concat([df1,df2]) - 'combine df'\n"
        "[2] list(df) - 'show all column name'\n"
        "[3] 'remove duplicate rows'\n"
        "[4] 'delete columns'\n"
        "[5] 'filter dataset with conditions'\n"
        "[6] 'remove nan'\n"
    )


# bsfcmap | 20.dec.09
def bsfcmap(df, speed_name, torque_name, bsfc_name, title, level):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = np.array(df[speed_name])
    y = np.array(df[torque_name])
    z = np.array(df[bsfc_name])
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
def dutycycle(df, speed_name, torque_name, stepx, stepy, bubblesize, title):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = df[speed_name]
    y = df[torque_name]

    x1 = int((min(x) - 200) / 100) * 100
    x2 = int((max(x) + 200) / 100) * 100
    y1 = int((min(y) - 200) / 100) * 100
    y2 = int((max(y) + 200) / 100) * 100

    xedges = [*range(x1, x2, stepx)]
    yedges = [*range(y1, y2, stepy)]

    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    hist = hist_temp.T
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.set_xticks(xedges, minor=False)
    ax.set_yticks(yedges, minor=False)

    ax.grid(which='both', color='grey', linestyle='--', alpha=0.6)

    ax.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.5)
    ax.set_xlabel(speed_name)
    ax.set_ylabel(torque_name)
    ax.set_title(title)
    plt.show()


# dutycycle3d plot | 20.dec.14
def dutycycle3d(df,speed_name, torque_name, barnum, title):
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import pandas as pd
#     %matplotlib notebook

    # define inputs.
    df = df

    x = df[speed_name]
    y = df[torque_name]
    bins = barnum
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


# boxplot01 (single boxplot, 1 parameter, details info) | 20.dec.14
def boxplot01(df, parameter_name, title):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df

    # data = pd.read_csv('demo.csv')
    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    #     ax1.set_xlabel(parameter_name)
    labels = [parameter_name]

    par = df[parameter_name]

    red_square = dict(markerfacecolor='red', marker='o', alpha=0.5, lw=1)

    B = ax1.boxplot(par, labels=labels, flierprops=red_square)
    # B = B.set(color='blue')
    x = [item.get_ydata() for item in B['whiskers']]

    # box_bdr=[]
    x1 = x[0][1]
    x2 = x[0][0]
    x3 = round(np.median(par), 2)
    x4 = x[1][0]
    x5 = x[1][1]

    box_bdr = [x1, x2, x3, x4, x5]

    for i in range(len(box_bdr)):
        plt.axhline(y=box_bdr[i], ls='--', alpha=0.5, c='darkorange', lw=1)
        plt.text(0.51, box_bdr[i], str(round(box_bdr[i], 2)), size=9, c='darkorange')

    # show mean and variation
    mean = round(np.mean(par))
    std_error = round(np.std(par))
    plt.axhline(y=mean, ls='--', alpha=0.5, c='blue', lw=1)
    plt.text(1.1, mean, '→ (mean:' + str(mean) + ' | std-err:' + str(std_error) + ')', size=9, c='blue')

    plt.show()


# boxplot02 (differrent parameter, same category)
def boxplot02(df, title):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    group = []
    medians = []
    std_err = []

    df = df

    # get all columns names, medians, std_errs
    for i in df.iloc[:, :].columns:
        dfi = df[i]
        group.append(dfi)
        medians.append(np.mean(df[i]))
        std_err.append(np.std(df[i]))

    # start chart layout
    fig1, ax1 = plt.subplots()

    num_boxes = len(list(df))
    pos = np.arange(num_boxes) + 1
    word_colors = ['steelblue', 'darkorange']

    # 01-show medium value
    upper_labels = ['Mean:' + str(np.round(s, 1)) for s in medians]

    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        #     k = tick % 2
        ax1.text(pos[tick], .96, upper_labels[tick],
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center', size='small',
                 weight='semibold', color=word_colors[0])

    # 02-show standard error value
    upper_labels = ['Std_Err:' + str(np.round(s, 1)) for s in std_err]

    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        #     k = tick % 2
        ax1.text(pos[tick], .93, upper_labels[tick],
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center', size='small',
                 weight='semibold', color=word_colors[1])

    # 03-change abnormal format
    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)
    bx = ax1.boxplot(group, flierprops=red_square, patch_artist=True)

    # 04-change boxplot colors:
    for patch in bx['boxes']:
        patch.set_facecolor('lightgrey')

    # 05-chart title
    ax1.set_title(title)

    # 06-change x ticks
    xticks = list(df)
    ax1.set_xticklabels(xticks, rotation=45, fontsize=8)

    # 07-add grid lines
    ax1.yaxis.grid(True)

    plt.show()


# boxplot03 (same parameter, different gategory)
def boxplot03(df, category_x_name, value_y_name, title):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    df = df

    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    group = []

    cat = list(set(df[category_x_name]))
    for i in cat:
        dfi = df.loc[df[category_x_name] == i]
        group.append(dfi[value_y_name])

    fig1, ax1 = plt.subplots()
    ax1.yaxis.grid(True)

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)
    bx = ax1.boxplot(group, flierprops=red_square, patch_artist=True)

    for patch in bx['boxes']:
        patch.set_facecolor('lightgrey')

    ax1.set_xticklabels(cat, rotation=45, fontsize=9, fontproperties=font)
    ax1.set_ylabel(value_y_name)
    plt.title(title)
    plt.show()


# pds dataset cleaning:
def pdsclean(df):
    # 1，turn '\N' into 'NaN';
    # 2.delete whole column with 'NaN';
    # 3.front fill & back fill;
    # 4.remove duplicate rows
    # (Format writing:  df=pdsclean(df))

    df = df

    # [step1]:turn \N into '' (empty value)
    for i in df.iloc[:, :].columns:
        df.loc[df[i] == '\\N', i] = 'NaN'

    # [step2]delete the whole column if any column still has na value.
    df.dropna(axis=1, how='all', inplace=True)

    # [step3]:fill empty value
    df = df.mask(df == 'NaN', None).ffill(axis=0)

    # [step4]:remove duplicate rows
    df = df.drop_duplicates()

    return df


# boxscatterplot









# Map (based on city + province, values)
# Histogram
# Histogram – normalized curve.
# Line plot
# Scatter
# Scatter + box
# Scatter + hist
# data analytics ppt里的图表
# python培训材料里的图表

# 多因子相关性矩阵图/