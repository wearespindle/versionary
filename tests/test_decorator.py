from pytest import raises

from versionary.decorators import versioned
from versionary.exceptions import DuplicateVersionException, InheritanceException, InvalidVersionException

from .utils.mixed_members import MixedClass, mixed_func
from .utils.versioned_members import MyClass, MyInheritanceClass, my_function, your_function
from .utils.versioned_members_with_number import MyClassNr, MyInheritanceClassNr, my_function_nr, your_function_nr


def test_decorator_for_functions_without_number():
    """
    Test the decorator for functions without a number.
    """
    assert my_function.v1() == 1
    assert my_function.v2() == 2


def test_decorator_for_classes_without_number():
    """
    Test the decorator for classes without a number.
    """
    assert MyClass.v1().hello() == 3
    assert MyClass.v2().hello() == 4


def test_decorator_for_class_inheritance_without_number():
    """
    Test the decorator for classes that inherit without a number.
    """
    assert MyInheritanceClass.v1().hello() == 5
    assert MyInheritanceClass.v1().parent() == 0
    assert MyInheritanceClass.v2().hello() == 6
    assert MyInheritanceClass.v2().parent() == 0


def test_unsupported_version_without_number():
    """
    Test the decorator when supplying a non existing version without a number.
    """
    with raises(InvalidVersionException):
        your_function.v3()


def test_inheritance_exception_without_number():
    """
    Test the decorator for wrongful inheritance without a number.
    """
    message = ('`MyClass` with version `4` is not allowed to inherit from '
               'version `1`! Can only inherit from previous version')

    with raises(InheritanceException) as excinfo:
        from .utils import without_number_inheritance  # noqa

    assert str(excinfo.value) == message


def test_inheritance_exception_proxy_without_number():
    """
    Test the decorator when inheriting from ProxyClass without a number.
    """
    message = 'Not allowed to inherit from `MyClass` without version!'

    with raises(InheritanceException) as excinfo:
        from .utils import without_number_inheritance_proxy  # noqa

    assert str(excinfo.value) == message


def test_duplicate_version_exception():
    """
    Test if the duplicate version exception is raised when importing.
    """
    with raises(DuplicateVersionException):
        from .utils import duplicate_versions  # noqa


def test_decorator_for_functions_with_number():
    """
    Test the decorator for functions with a number.
    """
    assert my_function_nr.v1() == 1
    assert my_function_nr.v2() == 2


def test_decorator_for_classes_with_number():
    """
    Test the decorator for classes with a number.
    """
    assert MyClassNr.v1().hello() == 3
    assert MyClassNr.v2().hello() == 4


def test_decorator_for_class_inheritance_with_number():
    """
    Test the decorator for classes that inherit with a number.
    """
    assert MyInheritanceClassNr.v1().hello() == 5
    assert MyInheritanceClassNr.v1().parent() == 0
    assert MyInheritanceClassNr.v2().hello() == 6
    assert MyInheritanceClassNr.v2().parent() == 0


def test_unsupported_version_with_number():
    """
    Test the decorator when supplying a non existing version with a number.
    """
    with raises(InvalidVersionException):
        your_function_nr.v3()


def test_inheritance_exception_with_number():
    """
    Test the decorator for wrongful inheritance with a number.
    """
    message = ('`MyClass` with version `4` is not allowed to inherit from '
               'version `1`! Can only inherit from previous version')

    with raises(InheritanceException) as excinfo:
        from .utils import with_number_inheritance  # noqa

    assert str(excinfo.value) == message


def test_inheritance_exception_proxy_with_number():
    """
    Test the decorator when inheriting from ProxyClass with a number.
    """
    message = 'Not allowed to inherit from `MyClass` without version!'

    with raises(InheritanceException) as excinfo:
        from .utils import with_number_inheritance_proxy  # noqa

    assert str(excinfo.value) == message


def test_mixed_usage():
    """
    Test mixed usage of decorator formats.
    """
    assert mixed_func.v1() == 1
    assert mixed_func.v2() == 2
    assert mixed_func.v3() == 3
    assert mixed_func.v4() == 4

    assert MixedClass.v1().hello() == 5
    assert MixedClass.v2().hello() == 6
    assert MixedClass.v3().hello() == 7
    assert MixedClass.v4().hello() == 8


def test_invalid_number_type():
    """
    Test using the decorator with a invalid number type.
    """
    message = 'Only integers allowed as version!'

    with raises(InvalidVersionException) as excinfo:
        @versioned('a')
        def my_wrong_versioned():
            return 1

    assert str(excinfo.value) == message

def test_latest():
    """
    Test using the latest() function
    """

    @versioned(1)
    class Foo:
        def __init__(self, passedin=None):
            self.local_thing = passedin

        def cls_mthd():
            return "Foo version 1"
        
        def rad(self):
            return f"dad: {self.local_thing}"

    @versioned(2)
    class Foo:
        def __init__(self, passedin=None):
            self.local_thing = passedin

        def cls_mthd():
            return "Foo version 2"

        def rad(self):
            return f"racer: {self.local_thing}"
    
    assert Foo.v1("bod").rad() == "dad: bod"
    assert Foo.v2("car").rad() == "racer: car"
    assert Foo.latest("speed").rad() == "racer: speed"
    assert Foo.latest().__class__.cls_mthd() == "Foo version 2"
    