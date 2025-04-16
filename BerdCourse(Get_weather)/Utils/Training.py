# numbers = list(range(11))
# print(numbers)
# for i in range(len(numbers)):
#    numbers[i] += 1
# print(numbers)

# numb = [i % 10 for i in range(100) if i % 5 == 0]
# print(numb)


# import matplotlib.pyplot as plt
#
# X = [1, 12, 23,12, 65, 23,32,56,89]
# Y = [23, 8, 11,15, 23, 48,2,5,3]
#
# plt.plot(X, Y)
#
# plt.show()


import numpy as np

a = (np.arange(1, 26).reshape(5, 5))
print(a)
print(a.shape)
print(a.ndim)




