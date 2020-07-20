import numpy as np
import py_cuffs
import matplotlib.pyplot as plt
import cupy as cp
from matplotlib.widgets import Slider
import sys
import fss_py3 as fss_py
import HITEMP_spectra

v_min,v_max = 1800.0,2400.0 #cm-1
dv = 0.002 #cm-1
v_arr = np.arange(v_min,v_max,dv)
N_v = len(v_arr)
N_wG, N_wL = 4, 8

py_cuffs.set_path('C:/CDSD4000/npy/')
py_cuffs.set_N_lines(int(2.2E8))
py_cuffs.init(v_arr,N_wG,N_wL)


p = 1.1 #bar
T = 300.0 #K

##plt.axhline(0,c='k',lw=1)
##plt.axhline(1,c='k',lw=1)
spectrum_h = py_cuffs.iterate(p, T)
##spectrum_h = 10**-spectrum_h
p1, = plt.plot(v_arr,spectrum_h, "-",linewidth=1)

plt.yscale('log')
plt.xlim(2400,2200)
plt.subplots_adjust(bottom=0.20)

axcolor = 'lightgoldenrodyellow'
temp_ax = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
temp_slider = Slider(temp_ax, 'T(K)', 50, 5000, valinit=T)

def update(val):
    T = temp_slider.val
    spectrum_h = py_cuffs.iterate(p, T)
##    spectrum_h = 10**-spectrum_h
    p1.set_ydata(spectrum_h)
    plt.gcf().canvas.draw_idle()

temp_slider.on_changed(update)


plt.show()
cp._default_memory_pool.free_all_blocks()
