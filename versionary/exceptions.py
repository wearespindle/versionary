class InvalidVersionException(Exception):
    """
    Exception thrown when providing a version of a class/function that
    does not exists.
    """
    pass


class InterruptedVersioningException(InvalidVersionException):
    """
    Exception used when there is a gap in the versioning or the versioning
    did not start at version 1.
    """
    pass


class DuplicateVersionException(InvalidVersionException):
    """
    Exception thrown when trying define the same version for a function
    or class twice.
    """
    pass


class InheritanceException(InvalidVersionException):
    """
    Exception thrown when inheriting from the wrong version of the class.
    """
    pass


class MissingDecoratorException(Exception):
    """
    Exception thrown when a @versioned decorator is missing.
    """
    pass


class NotCallableException(Exception):
    """
    Raised when trying to call the ProxyClass which shouldn't be called.
    """
    pass
