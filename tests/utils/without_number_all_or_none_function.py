from versionary.decorators import versioned


@versioned()
def my_function():
    return 1


def my_function_v2():
    return 2


@versioned()
def your_function():
    return 3


@versioned()
def your_function_v2():
    return 4
