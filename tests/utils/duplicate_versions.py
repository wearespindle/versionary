from versionary.decorators import versioned


@versioned()
def my_func():
    pass


@versioned()
def my_func_v2():
    pass


@versioned()  # noqa
def my_func_v2():
    pass
