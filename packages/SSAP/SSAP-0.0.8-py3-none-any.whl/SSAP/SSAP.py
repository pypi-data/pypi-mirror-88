# Author:tony
# Create time:2020.12.09
# The software is build 4 SSAP POC testing.

# %Dev plan: GUI, pop up web visualization, eng charts

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

# basic introduction of the pkg
def info():
    print('Welcome to SSAP! SSAP→[Self Service Analytics Platform]. There are different analytics function modules to '
          'support you complete different data analytics scenarios. Please enjoy! Any question or support needed, '
          'please raise in Big Data Community(BDC).')
