from versionary.decorators import versioned


@versioned(1)
def my_function():
    return 1


@versioned(3)  # noqa
def my_function():
    return 3
