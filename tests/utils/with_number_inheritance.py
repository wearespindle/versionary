from versionary.decorators import versioned


@versioned(1)
class MyClass(object):
    pass


@versioned(2)
class MyClass(MyClass.v1):
    pass


@versioned(3)
class MyClass(MyClass.v2):
    pass


@versioned(4)
class MyClass(MyClass.v1):
    pass
