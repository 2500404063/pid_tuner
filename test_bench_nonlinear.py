import math
import pid
import numpy as np
from matplotlib import pyplot as plt
import aircraft as ac

x = np.linspace(1, 100, 2000)
signal = np.log(x)  # + np.power(x, 2)
for i in range(200):
    signal[i*10] = signal[i*10] + np.random.normal(0, 0.01)

pid_param = pid.PosPID_Param()
pid_param.kp = 1.701  # 1.701  # 0.900  # 0.4  # 1.2  # 5.91999
pid_param.ki = 0.1  # 0.050000  # 0.04200  # 0.0259999999  # 0.007  # 0.00555
pid_param.kd = 97  # 90  # 99.2999  # 99.9999  # 65.2000  # 59  # 52


plt.plot(x, signal)
test_y = list()
ac.h = 0
for i in range(2000):
    err = ac.h - signal[i]
    u = pid.PosPID_Iterate(pid_param, 0, err)
    ac.set_a(u)
    ac.f()
    test_y.append(ac.h)
plt.plot(x, test_y)
plt.show()
