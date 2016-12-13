from versionary.decorators import versioned


@versioned()
class MyClass(object):
    pass


@versioned()
class MyClassV2(MyClass):
    pass
