# ATK Interface for Python

3 steps to call ATK with Python
```python
conID = atkOpen()
atkConnect(conID, "Command", "Parameters")
atkClose(conID)
```
You can found the basic operations in `ATKCommandWrapper`.
