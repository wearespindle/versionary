from versionary.decorators import versioned


@versioned(1)
def my_function():
    return 1


def my_function():  # noqa
    return 2


@versioned(1)
def your_function():
    return 3


@versioned(2)  # noqa
def your_function():
    return 4
