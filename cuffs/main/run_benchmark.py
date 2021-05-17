import numpy as np
import py_cuffs
import matplotlib.pyplot as plt
import cupy as cp
from matplotlib.widgets import Slider
import sys
import fss_py3 as fss_py
import HITEMP_spectra
from time import perf_counter
import pandas as pd

v_min,v_max = 1800.0,2400.0 #cm-1
dv = 0.002 #cm-1
v_arr = np.arange(v_min,v_max,dv)
N_v = len(v_arr)
N_wG, N_wL = 4, 8

p = 1.0 #bar

N_arr = [1e4,1e4,1e5,1e6,2.01e6,5.01e6,1e7,2e7,5e7,1e8,2e8]

t_init_biglist = []
t_iter_biglist = []
py_cuffs.set_path('C:/CDSD4000/npy/')

for N in N_arr:


    t_init_list = []
    t_iter_list = []

    t_init = perf_counter()


    py_cuffs.set_N_lines(int(N))
    py_cuffs.init(v_arr,N_wG,N_wL)

    for T in np.arange(300,3000,100):
        t_iter = perf_counter()
        spectrum_h = py_cuffs.iterate(p, T)
        t_iter = perf_counter() - t_iter
        t_iter_list.append(t_iter)
        
    t_iter_biglist.append(np.mean(t_iter_list[1:]))

    t_init = perf_counter() - t_init - np.sum(t_iter_list[1:])
    t_init_biglist.append(t_init)

    cp._default_memory_pool.free_all_blocks()



df = pd.DataFrame({'N':N_arr[1:],
                   't_init (s)':t_init_biglist[1:],
                   't_iter (s)':t_iter_biglist[1:]})
df.to_excel('benchmark_output.xlsx')

plt.plot(N_arr[1:],t_init_biglist[1:],'o--')
plt.plot(N_arr[1:],t_iter_biglist[1:],'o--')
plt.yscale('log')
plt.xscale('log')
plt.grid(True)

plt.show()
