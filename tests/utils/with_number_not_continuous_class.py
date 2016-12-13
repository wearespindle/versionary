from versionary.decorators import versioned


@versioned(1)
class MyClass():

    def hello():
        return 1


@versioned(3)  # noqa
class MyClass():

    def hello():
        return 3
