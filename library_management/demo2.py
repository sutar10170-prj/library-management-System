def mydecorator(func):
    def wap():
        print("one")
        func()
        print("two")
    return wap 