from versionary.decorators import versioned


@versioned()
def my_function():
    return 1


@versioned()
def my_function_v2():
    return 2


@versioned()
class MyClass(object):

    def hello(self):
        return 3


@versioned()
class MyClassV2(object):

    def hello(self):
        return 4


@versioned()
class MyInheritanceClass(object):

    def parent(self):
        return 0

    def hello(self):
        return 5


@versioned()
class MyInheritanceClassV2(MyInheritanceClass.v1):

    def hello(self):
        return 6


@versioned()
def your_function():
    return 7


@versioned()
def your_function_v2():
    return 8
