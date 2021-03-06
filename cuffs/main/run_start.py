import numpy as np
import py_cuffs
import matplotlib.pyplot as plt
import cupy as cp
from matplotlib.widgets import Slider
import sys
import fss_py3 as fss_py
import HITEMP_spectra
from time import perf_counter

v_min,v_max = 1800.0,2400.0 #cm-1
dv = 0.002 #cm-1
v_arr = np.arange(v_min,v_max,dv)
N_v = len(v_arr)
N_wG, N_wL = 4, 8

py_cuffs.set_path('C:/CDSD4000/npy/')
py_cuffs.set_N_lines(int(2.3E8))
py_cuffs.init(v_arr,N_wG,N_wL)


p =     0.1 #bar
T = 3000.0 #K

##plt.axhline(0,c='k',lw=1)
##plt.axhline(1,c='k',lw=1)
spectrum_h = py_cuffs.iterate(p, T)
##spectrum_h = 10**-spectrum_h
spectrum_h /= np.max(spectrum_h)
##spectrum_h *= np.log(10)
p1, = plt.plot(v_arr,spectrum_h, "k-",linewidth=0.5)
ax = plt.gca()
##plt.yscale('log')
plt.xlim(2400,2200)
plt.subplots_adjust(bottom=0.20)

axcolor = 'lightgoldenrodyellow'
temp_ax = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
temp_slider = Slider(temp_ax, 'T(K)', 50, 5000, valinit=T)

def update(val):
    T = temp_slider.val
    t0 = perf_counter()
    spectrum_h= py_cuffs.iterate(p, T)
    t0 = perf_counter() - t0
##    spectrum_h = 10**-spectrum_h
    spectrum_h /= np.max(spectrum_h)
    p1.set_ydata(spectrum_h)
    ax.set_title('T = {:.2f} K ({:.2f} ms)'.format(T,1e3*t0))
    plt.gcf().canvas.draw_idle()

temp_slider.on_changed(update)


plt.show()
cp._default_memory_pool.free_all_blocks()
