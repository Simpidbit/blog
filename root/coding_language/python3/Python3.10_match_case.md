# Python 3.10 新特性：match...case

在Python3.10之前，
Python没有内置的像其他语言的switch那样的模式匹配功能，
人们只能用if...elif...else来模拟所谓 "switch" 的功能。
Python3.10之后，加入了match...case语句，就是Python的 "switch" 功能


语法:
```python
match var:
    case var1:
        <action1>       # 每个case执行完要执行的语句后不需要加break，Python解释器会自动帮你break
    case var2:
        <action2>
    case var3:
        <action3>

    ......

    case _:         # case _ 就相当于其他语言中的default
        <default action>
```



例如：
```python
match input("输入一个数字"):
    case 1:
        print("你输入的是1")
    case 2:
        print("你输入的是2")
    case _:
```

