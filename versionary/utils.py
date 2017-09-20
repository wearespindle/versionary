import inspect
import logging
import re

from six import with_metaclass

from .exceptions import InvalidVersionException, NotCallableException

CLASS, FUNCTION = 0, 1
CLASS_VERSION_TAG = 'V'
CLASS_SUFFIX_RE = '(?P<suffix>%s)(?P<version>\d+)$' % CLASS_VERSION_TAG
FUNCTION_VERSION_TAG = '_v'
FUNCTION_SUFFIX_RE = '(?P<suffix>%s)(?P<version>\d+)$' % FUNCTION_VERSION_TAG
PROXY_VERSION_TAG = 'v'
PROXY_VERSION_RE = '^(?P<suffix>%s)(?P<version>\d+)$' % PROXY_VERSION_TAG

logger = logging.getLogger('versionary_logger')


def determine_member_type(member):
    """
    Function to determine the type of a member.

    Args:
        member (class|function): The member to check for.

    Returns:
        int: Value for class or function.
    """
    if inspect.isfunction(member):
        member_type = FUNCTION
    elif inspect.isclass(member):
        member_type = CLASS
    else:
        raise NotImplementedError('Only classes or functions are supported!')

    return member_type


def create_proxy_class(base_name):
    """
    Function to create a proxy class to be able to set attributes to.
    This is used to make my_func.v1() or MyClass.v1() possible.

    Args:
        base_name (str): Name to be used as reference to the original
            member. Used for logging purposes.

    Returns:
        class: The ProxyClass.
    """
    class ProxyType(type):
        """
        Custom type to be able to override __getattr__ and
        __getattribute__ on the static ProxyClass.
        """

        def __getattribute__(cls, name):
            """
            Log when a certain version is called.
            """
            version_attr_re = re.compile(PROXY_VERSION_RE)

            if version_attr_re.search(name):
                attr = type.__getattribute__(cls, name)
                logger.info('Called `%s` for `%s`', name, cls._base_name)
                return attr

            return type.__getattribute__(cls, name)

        def __getattr__(cls, name):
            """
            This method is called when accessing non-existing attributes. When
            attempting to access versioning attributes (.vX), raise an
            InvalidVersionException instead of the usual AttributeError.
            """
            version_attr_re = re.compile(PROXY_VERSION_RE)

            if version_attr_re.search(name):
                message = 'Invalid version `%s` for `%s`' % (name, cls._base_name)
                raise InvalidVersionException(message)

            raise AttributeError('%r has no attribute %r' %
                                 (cls._base_name, name))

    setattr(ProxyType, '_base_name', base_name)

    class ProxyClass(with_metaclass(ProxyType)):
        """
        ProxyClass that holds all the versions for a certain class or function.
        """
        _is_versioned = True

        def __init__(self):
            message = 'Cannot call `{name}` directly, use versioned attributes instead (`{name}`.vX)'.format(
                name=self.__class__._base_name)
            raise NotCallableException(message)

    return ProxyClass
