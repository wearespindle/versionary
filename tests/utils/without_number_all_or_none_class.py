from versionary.decorators import versioned


@versioned()
class MyClass():

    def hello():
        return 1


class MyClassV2():

    def hello():
        return 2
