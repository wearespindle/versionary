from versionary.decorators import versioned


@versioned(1)
class MyClass(object):
    pass


@versioned(2)
class MyClass(MyClass):
    pass
