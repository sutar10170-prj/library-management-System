from demo2 import mydecorator


@mydecorator
def say():
    print("hello")

say()