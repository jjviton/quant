# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 23:47:55 2022

@author: INNOVACION
"""

import tkinter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   




import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()