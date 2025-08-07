def fact(x):
    res = 1
    for i in range(2, x + 1):
        res = res * i
    return res


def fibo(x):
    a = 0
    b = 1
    for i in range(x):
        a = b
        b = a + b
    return a
