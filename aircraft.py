import time
import threading

g = 12.0  # 6.0
a = 0.0
h = 0.0
v = 0.0


def f():
    global h
    global v
    global g
    global a
    v = v + (a - g) * 0.1
    h = h + v * 0.1
    h = 0 if h < 0 else h
    v = 0 if v < 0 else v


def set_a(F):
    global a
    a = F


th = threading.Thread(target=f)
th.start()
