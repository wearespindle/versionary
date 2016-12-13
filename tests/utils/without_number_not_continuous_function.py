from versionary.decorators import versioned


@versioned()
def my_function():
    return 1


@versioned()
def my_function_v3():
    return 3
