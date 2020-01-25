import numpy as np

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [[10], [11], [12]]
A = np.array(a)
B = np.array(b)
AA = A[1:][..., 1:]
BB = B[1:]
print('AA=', AA)
print('A=', A)
print('BB=', BB)
print('B=', B)
