import numpy as np
x=np.array([23,4,5,3,23])
for i in range(5):
    x=x+i
    plt.subplot()
    plt.plot(x)

