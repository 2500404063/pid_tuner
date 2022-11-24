import math


class PosPID_Param:
    kp = 0.0
    ki = 0.0
    kd = 0.0
    I = 0.0
    e1 = 0.0


class DeltaPID_Param:
    kp = 0.0
    ki = 0.0
    kd = 0.0
    e1 = 0.0
    e2 = 0.0


"""
Coordinate:
 e
+|
 |
 |------------------
 |
-|__________________
e<0: u↑
e>0: u↓
kp,ki,kd >= 0
"""


def PosPID_Iterate(params: PosPID_Param, r, y):
    u = 0.0
    e = r - y
    params.I = params.I + e
    u = params.kp * e
    u += params.ki * params.I
    u += params.kd * (e - params.e1)
    params.e1 = e
    return u


def DeltaPID_Iterate(params: DeltaPID_Param, r, y):
    e = r - y
    deltaU = 0
    deltaU = params.kp * (e - params.e1)
    deltaU += params.ki * (e)
    deltaU += params.kd * (e - 2 * params.e1 - params.e2)
    params.e2 = params.e1
    params.e1 = e
    return deltaU
