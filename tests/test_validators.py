from pytest import raises

from versionary.exceptions import InterruptedVersioningException, MissingDecoratorException
from versionary.validators import validate_module_versioning

from .utils import (
    with_number_all_or_none_class,
    with_number_all_or_none_function,
    with_number_not_continuous_class,
    with_number_not_continuous_function,
    without_number_all_or_none_class,
    without_number_all_or_none_function,
    without_number_not_continuous_class,
    without_number_not_continuous_function,
)


def test_versioned_all_or_none_function():
    """
    Test all or none versioning for the versioned decorator on functions.
    """
    module_name = without_number_all_or_none_function.__name__

    with raises(MissingDecoratorException):
        validate_module_versioning(module_name)

    module_name = with_number_all_or_none_function.__name__

    with raises(MissingDecoratorException):
        validate_module_versioning(module_name)


def test_versioned_all_or_none_class():
    """
    Test all or none versioning for the versioned decorator on classes.
    """
    module_name = without_number_all_or_none_class.__name__

    with raises(MissingDecoratorException):
        validate_module_versioning(module_name)

    module_name = with_number_all_or_none_class.__name__

    with raises(MissingDecoratorException):
        validate_module_versioning(module_name)


def test_versioned_not_continuous_function():
    """
    Test non continuous versioning for the versioned decorator on functions.
    """
    module_name = without_number_not_continuous_function.__name__

    with raises(InterruptedVersioningException):
        validate_module_versioning(module_name)

    module_name = with_number_not_continuous_function.__name__

    with raises(InterruptedVersioningException):
        validate_module_versioning(module_name)


def test_versioned_not_continuous_class():
    """
    Test non continuous versioning for the versioned decorator on classes.
    """
    module_name = without_number_not_continuous_class.__name__

    with raises(InterruptedVersioningException):
        validate_module_versioning(module_name)

    module_name = with_number_not_continuous_class.__name__

    with raises(InterruptedVersioningException):
        validate_module_versioning(module_name)
