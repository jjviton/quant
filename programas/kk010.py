# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 18:54:41 2020

@author: INNOVACION
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


s = pd.Series([np.random.randint(1,100) for i in range(1,100)])
a=s.index
b=s.values

plt.plot(s.index, s.values)
