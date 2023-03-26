a = 31
for _ in range(10000):
    a = (a ** 2) % (10 ** 4000)
    print(a)