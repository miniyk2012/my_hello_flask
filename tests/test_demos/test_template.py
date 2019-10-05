def fibonacci(n):
    a, b = 1, 1
    i = 1
    while i <= n:
        a, b = b, a + b
        i += 1
    return a


def test_fabonaci():
    assert fibonacci(0) == 1
    assert fibonacci(1) == 1
    assert fibonacci(2) == 2
    assert fibonacci(3) == 3
    assert fibonacci(4) == 5
    assert fibonacci(5) == 8
    assert fibonacci(6) == 13


