from versionary.decorators import versioned


@versioned()
class MyClass(object):
    pass


@versioned()
class MyClassV2(MyClass.v1):
    pass


@versioned()
class MyClassV3(MyClass.v2):
    pass


@versioned()
class MyClassV4(MyClass.v1):
    pass
