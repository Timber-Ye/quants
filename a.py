def test():
    for i in range(10):
        yield i

for i in test():
    print(i)