# ATK Interface for Python

Python调用ATK的三步核心操作
```python
from ATKConnectModule import atkOpen, atkConnect, atkClose

conID = atkOpen()                              # Connect to ATK
atkConnect(conID, "Command", "Parameters")     # Run an ATK command
atkClose(conID)                                # Disconnect from ATK
```
命令都在ATKCommandWrapper里，涉及ATK调用的操作有如下几项：
- atkOpen
- atkClose
- 创建一个卫星
- 给某颗卫星创建一个敏感器
- 给某个敏感器设置指向和投影高度
- 给某颗卫星设置轨道根数初值
- 给某颗卫星添加一个轨道预报段
- 给某颗卫星添加一个脉冲
- 运行当前机动规划方案（运行后机动规划才会生效）

测试算例是【ctoc13_c.py】，里面会有读txt的操作，txt的格式是这样的：

|$a_0$ | $e_0$  | $i_0$ | $\Omega_0$ | $\omega_0$ | $f_0$|
| -- | --| --| --|--|--|
|$t_1$ | $\Delta V_{x1}$ | $\Delta V_{y1}$ | $\Delta V_{z1}$|
|$t_2$ | $\Delta V_{x2}$ | $\Delta V_{y2}$  | $\Delta V_{z2}$|

