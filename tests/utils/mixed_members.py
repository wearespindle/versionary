from versionary.decorators import versioned


@versioned(1)
def mixed_func():
    return 1


@versioned()
def mixed_func_v2():
    return 2


@versioned()
def mixed_func_v3():
    return 3


@versioned(4)  # noqa
def mixed_func():
    return 4


@versioned()
class MixedClass(object):

    def hello(self):
        return 5


@versioned(2)  # noqa
class MixedClass(object):

    def hello(self):
        return 6


@versioned(3)  # noqa
class MixedClass(object):

    def hello(self):
        return 7


@versioned()
class MixedClassV4(object):

    def hello(self):
        return 8
