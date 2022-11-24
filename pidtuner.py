import math
import pid
import numpy as np
from matplotlib import pyplot as plt
import aircraft as ac

x = np.linspace(0, 99, 100)
signal = np.hstack([[10]*100])

pid_param = pid.PosPID_Param()
pid_param.kp = 0  # 0.4  # 1.2  # 5.91999
pid_param.ki = 0  # 0.0259999999  # 0.007  # 0.00555
pid_param.kd = 0  # 65.2000  # 59  # 52


class PIDTuner:
    def __init__(self) -> None:
        self.AveErr = 0
        self.LastAveErr = 0
        self.DeltaAveErr = 0
        self.Count = 0
        # P
        self.FlagP = False
        self.RangP = [0, 7]
        self.IncP = 0.1
        self.DesP = 0.01
        self.ConP = 0.001
        # I
        self.FlagI = False
        self.RangI = 0.00001
        self.ConI = 0.001
        # D
        self.FlagD = False
        self.ConD = 0.1

    def Reset(self):
        self.AveErr = 0
        self.DeltaAveErr = 0
        self.Count = 0

    def CountPeak(self, err):
        self.Count = self.Count + 1
        self.LastAveErr = self.AveErr
        self.DeltaAveErr = (err - self.AveErr) / self.Count
        self.AveErr = self.AveErr + self.DeltaAveErr

    def Tune(self):
        self.deltaP = 0
        self.deltaI = 0
        self.deltaD = 0
        # P Tuner
        if self.FlagP == False:
            if abs(self.AveErr) > self.RangP[1]:
                self.deltaP = self.IncP * abs(self.AveErr - self.RangP[1]) + self.ConP
            elif abs(self.AveErr) < self.RangP[0]:
                self.deltaP = -self.DesP * abs(self.AveErr - self.RangP[0]) - self.ConP
            else:
                self.deltaP = 0
                self.FlagP = True
        # I Tuner
        if self.FlagP == True and not self.FlagI:
            if abs(self.AveErr) > self.RangI:
                self.deltaI = self.ConI
            else:
                self.deltaI = 0
                self.FlagI = True
        # D Tuner
        if self.FlagP and self.FlagI and not self.FlagD:
            self.deltaD = self.ConD
        return (self.deltaP, self.deltaI, self.deltaD)


tuner = PIDTuner()

fig0 = plt.figure(0)
ax0 = fig0.add_axes([0.1, 0.1, 0.8, 0.8])
fig1 = plt.figure(1)
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
data0_x = list()
data0_y = list()
AveErrSum = 0
for m in range(1000000):
    tuner.Reset()
    ax0.cla()
    ax1.cla()
    ax0.plot(x, signal)
    test_x = list()
    test_y = list()
    ac.h = 0
    data0_x.append(m)
    for i in range(100):
        err = ac.h - 10
        tuner.CountPeak(err)
        u = pid.PosPID_Iterate(pid_param, 0, err)
        ac.set_a(u)
        ac.f()
        test_x.append(i)
        test_y.append(ac.h)
    # Tune
    deltaP, deltaI, deltaD = tuner.Tune()
    pid_param.kp = pid_param.kp + deltaP
    pid_param.ki = pid_param.ki + deltaI
    pid_param.kd = pid_param.kd + deltaD
    data0_y.append(tuner.AveErr)
    print(f'AveErr={tuner.AveErr}, P={pid_param.kp}, I={pid_param.ki}, D={pid_param.kd}, Delta: {deltaP}, {deltaI}, {deltaD}')
    ax0.plot(test_x, test_y)
    ax1.plot(data0_x, data0_y)
    plt.pause(0.005)
