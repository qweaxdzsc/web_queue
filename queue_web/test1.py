def test(var):
    return 1/(var**0.5)


a = test(63) + test(125) + test(160) + test(160) + test(500) + test(30)
x = 1 / a**2
print(x, a)