from versionary.decorators import versioned


@versioned(1)
def my_function_nr():
    return 1


@versioned(2)  # noqa
def my_function_nr():
    return 2


@versioned(1)
class MyClassNr(object):

    def hello(self):
        return 3


@versioned(2)  # noqa
class MyClassNr(object):

    def hello(self):
        return 4


@versioned(1)
class MyInheritanceClassNr(object):

    def parent(self):
        return 0

    def hello(self):
        return 5


@versioned(2)
class MyInheritanceClassNr(MyInheritanceClassNr.v1):

    def hello(self):
        return 6


@versioned(1)
def your_function_nr():
    return 7


@versioned(2)  # noqa
def your_function_nr():
    return 8
