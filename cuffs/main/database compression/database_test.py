import numpy as np
import gzip

fpath = 'C:/CDSD4000/npy/'


N = 1000

total_u = 0
total_c = 0

for arr_name in ['da','El','log_2gs','log_2vMm','na','S0','v0']:

    arr = np.load(fpath+arr_name + '.npy')

    bytesarr_uncompressed = bytes(arr[:N])
    bytesarr_compressed = gzip.compress(bytesarr_uncompressed)

    len_u = len(bytesarr_uncompressed)
    len_c = len(bytesarr_compressed)

    total_u += len_u
    total_c += len_c

    print(arr_name,len_u,len_c,len_c/len_u)
    print('min:',np.min(arr),'max:',np.max(arr))
    print('')
print('total:', total_u, total_c, total_c/total_u)
