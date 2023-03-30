from pytest import raises

from versionary.exceptions import InvalidVersionException, NotCallableException
from versionary.utils import CLASS, create_proxy_class, determine_member_type, FUNCTION


def test_determine_member_type():
    """
    Test the determine_member_type function when providing different types.
    """
    class MyClass(object):
        pass

    def my_func():
        pass

    my_var = 'my var'

    assert determine_member_type(MyClass) is CLASS
    assert determine_member_type(my_func) is FUNCTION

    with raises(NotImplementedError):
        determine_member_type(my_var)


def test_create_proxy_class():
    """
    Test the create_proxy_class function for logging, and exceptions.
    """
    base_name = 'base_name'

    proxy = create_proxy_class(base_name, 123)

    message = 'Cannot call `base_name` directly, use versioned attributes instead (`base_name`.vX)'

    with raises(NotCallableException) as excinfo:
        proxy()

    assert str(excinfo.value) == message

    setattr(proxy, 'v1', 'my_attr')

    assert proxy.v1 == 'my_attr'

    message = 'Invalid version `%s` for `%s`' % ('v2', base_name)
    with raises(InvalidVersionException) as excinfo:
        proxy.v2()

    assert str(excinfo.value) == message
