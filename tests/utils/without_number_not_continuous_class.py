from versionary.decorators import versioned


@versioned()
class MyClass():

    def hello():
        return 1


@versioned()
class MyClassV3():

    def hello():
        return 3
