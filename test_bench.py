import math
import pid
import numpy as np
from matplotlib import pyplot as plt
import aircraft as ac

x = np.linspace(0, 1999, 2000)
signal = np.hstack([[10]*500, [30]*500, [200]*500, [500]*500])

pid_param = pid.PosPID_Param()
pid_param.kp = 1.701  # 0.900  # 0.4  # 1.2  # 5.91999
pid_param.ki = 0.071000  # 0.04200  # 0.0259999999  # 0.007  # 0.00555
pid_param.kd = 99.9999  # 99.9999  # 65.2000  # 59  # 52


plt.plot(x, signal)
test_x = list()
test_y = list()
ac.h = 0
for i in range(2000):
    err = ac.h - signal[i]
    u = pid.PosPID_Iterate(pid_param, 0, err)
    ac.set_a(u)
    ac.f()
    test_x.append(i)
    test_y.append(ac.h)
plt.plot(test_x, test_y)
plt.show()
