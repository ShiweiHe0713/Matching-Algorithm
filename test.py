import numpy as np

arr = np.array([1,4,3,15,7])
sorted_indices = np.argsort(arr)
print(arr[sorted_indices][::-1])