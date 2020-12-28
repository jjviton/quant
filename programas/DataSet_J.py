# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:18:08 2020

@author: INNOVACION
"""
import pandas as pd
import numpy as np

np.random.seed(0)
# create an array of 5 dates starting at '2015-02-24', one per minute
rng = pd.date_range('2015-02-24', periods=5, freq='T')
df_test01 = pd.DataFrame({ 'Date': rng, 'Val': np.random.randn(len(rng)) }) 
#print (df_test01)
df_test02 = pd.DataFrame()
# Set the seed for a reproducible sample
np.random.seed(0)  
df_test02 = pd.DataFrame(np.random.randn(5, 3), columns=list('ABC'))
#print (df_test02)


df_test04= pd.DataFrame ([12,7,4,5,6])
#print(df_test04)


df_test05=  pd.DataFrame( range(2000),columns=list('p'))
df_test06 = pd.DataFrame(np.random.randint(-6, 6,size=(2000, 1)),columns=list('p'))
#df =       pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
#df_test06=  df_test06.reshape(-1,1)
df_test07=df_test05.add(df_test06)
#print( df_test07)

df_test03= pd.DataFrame ([1,
3,
5,
7,
0,
11,
13,
15,
7,
19,
21,
6,
8,
10,
13,
17,
23,
30,
39,
51,
66,
30,
28,
30,
30,
35,
30,
30,
30,
56,
30,
30,
30,
15,
7,
3,
1,
32,
33,
23,
12,
9,
18,
30,
43,
27,
14,
6,
15,
27,
40,
30,
18,
10,
6,
4,
12
],columns=list('p'))
#print(df_test03)
