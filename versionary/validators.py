import inspect
import re
import sys

from six import iteritems

from .exceptions import (
    InheritanceException, InterruptedVersioningException, MissingDecoratorException)
from .utils import CLASS_SUFFIX_RE, FUNCTION_SUFFIX_RE


def validate_module_versioning(module_name):
    """
    Function to validate the versioning of all members for a given module.

    Args:
        module_name (str): The name of the module.
    """
    module = sys.modules[module_name]

    _validate_continuous_versioning(module)
    _validate_missing_versioned_tags(module)


def validate_inheritance_for_class(cls):
    """
    Function to validate if the provided class inherits from the
    previous version of the class.

    Args:
        cls (class): The class to validate inheritance for.

    Raises:
        InheritanceException: When inherited from the wrong version.
    """
    # Skip all non versioned classes.
    if hasattr(cls, '__version__'):
        # Strip the name from the version suffix.
        class_suffix = re.compile('V\d+$')
        class_base_name = class_suffix.split(cls.__name__)[0]

        for base in cls.__bases__:
            # Inheriting from ProxyClass is not allowed.
            if base.__name__ == 'ProxyClass':
                message = 'Not allowed to inherit from `%s` without version!' % class_base_name
                raise InheritanceException(message)

            # Skip base classes that are not versioned.
            if hasattr(base, '__version__'):
                # Strip the name from the version suffix.
                base_base_name = class_suffix.split(base.__name__)[0]

                # If the inherited class has the same base name and
                # isn't the previous version of the provided class raise exception.
                if class_base_name == base_base_name:
                    if base.__version__ != cls.__version__ - 1:
                        message = ('`%s` with version `%s` is not allowed to inherit from '
                                   'version `%s`! Can only inherit from previous version' % (
                                       class_base_name,
                                       cls.__version__,
                                       base.__version__,
                                   ))
                        raise InheritanceException(message)


def _validate_continuous_versioning(module):
    """
    Validate if there are no gaps in the versioning of functions and
    classes for the given module.

    Args:
        module (module): The module to check for.

    Raises:
        InterruptedVersioningException: When there is a gap in the versioning
            of a function or class.
    """
    version_table = getattr(module, '__version_table__', {})

    # Loop all functions or classes with their given version mappings.
    for member_name, version_mapping in iteritems(version_table):
        # Get versions and sort them.
        versions = list(version_mapping['members'])
        versions.sort()

        # Check if there are gaps in the versions or if it does not start at 1.
        if versions != list(range(1, len(versions) + 1)):
            missing_versions = list(set(range(1, len(versions) + 1)) - set(versions))
            error = ('Versions need to be consecutive and start at `1`, missing version `%s`'
                     ' for `%s` in file `%s`' % (
                         missing_versions,
                         member_name,
                         module.__file__,
                     ))
            raise InterruptedVersioningException(error)


def _validate_missing_versioned_tags(module):
    """
    Function to validate if there any version tags missing which would lead
    to overriding versioned members and very dangerous behaviour!

    Args:
        module (module): The module to check for.

    Raises:
        MissingDecoratorException: When there is a decorator missing on
            a function or class.
    """
    version_table = getattr(module, '__version_table__', {})

    # Get all functions from the module.
    functions = inspect.getmembers(module, inspect.isfunction)
    functions_dict = dict(functions)
    function_names = list(functions_dict)

    # Get all classes from the module.
    classes = inspect.getmembers(module, inspect.isclass)
    classes_dict = dict(classes)
    class_names = list(classes_dict)

    for name in version_table.keys():
        msg = 'Both a versioned and unversioned `%s` exist in file `%s`!' % (name, module.__file__)
        class_pattern = re.compile('^%s%s' % (name, CLASS_SUFFIX_RE))
        func_pattern = re.compile('^%s%s' % (name, FUNCTION_SUFFIX_RE))
        class_matches = [class_pattern.search(_name) for _name in class_names if class_pattern.search(_name)]
        function_matches = [func_pattern.search(_name) for _name in function_names if func_pattern.search(_name)]

        # Check 1: @versioned() decorator on a function.
        # Check for duplicate names in classes or function names. Unversioned
        # functions appear in the funtions list whilst versioned appear in
        # the classes list. If the same name exists in both lists there's
        # a unversioned function.
        if (name in class_names or class_matches) and (name in function_names or function_matches):
            raise MissingDecoratorException(msg)

        # Check 2: @versioned(NUMBER) decorator on a function.
        # Versioned members are always a class due to the return of a
        # ProxyClass. If the name is in the version table there is a
        # decorated member. This filters decorated functions. If a function
        # is decorated and not decorated it shows in the functions list but
        # no longer in the classes list.
        if name not in class_names and name in function_names:
            raise MissingDecoratorException(msg)

        # Check 3: @versioned() or @versioned(NUMBER) decorator on a class.
        if name in class_names or class_matches:
            names_to_check = []
            # In case of suffix classes find all matching suffixed classes
            # to check.
            if class_matches:
                for match in class_matches:
                    names_to_check.append(match.group())
            else:
                names_to_check.append(name)

            # Check if all the listed classes are versioned.
            for key in names_to_check:
                if not getattr(classes_dict[key], '_is_versioned', False):
                    raise MissingDecoratorException(msg)
