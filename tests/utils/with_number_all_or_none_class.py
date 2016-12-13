from versionary.decorators import versioned


@versioned(1)
class MyClass():

    def hello():
        return 1


class MyClass():  # noqa

    def hello():
        return 2
