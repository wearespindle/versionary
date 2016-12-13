from collections import defaultdict
import re
import sys


from .exceptions import DuplicateVersionException, InvalidVersionException
from .utils import (CLASS, CLASS_SUFFIX_RE, create_proxy_class,
                    determine_member_type, FUNCTION, FUNCTION_SUFFIX_RE,
                    PROXY_VERSION_TAG)
from .validators import validate_inheritance_for_class


def versioned(number=None):
    """
    Decorator used to version a function or class.

    Usage 1:
        @versioned(1)
        my_func():
            pass

        @versioned(2)
        my_func():
            pass

    Usage 2:
        @versioned()
        my_func():
            pass

        @versioned()
        my_func_v2():
            pass

    Classes have the same usage only a different suffix:
        @versioned()
        MyClass(object):
            pass

        @versioned()
        MyClassV2(object):
            pass

    Args:
        number (int): The version number.

    Returns:
        class: ProxyClass with static methods (eg. v1, v2 etc.) for
            calling the versioned members respectively.
    """
    def wrap(member):
        """
        Wrap the member the decorator 'decorates'.

        Args:
            member (type): The member it decorates.

        Returns:
            ProxyClass: With members mapped to versions as staticmethods.
        """

        # Get the module of the member.
        module = sys.modules[member.__module__]

        # Get the version table that contains the versions for the members in
        # the module.
        version_table = getattr(module, '__version_table__', defaultdict(lambda: defaultdict(dict)))

        # Name of the member.
        name = member.__name__

        # Determine the type (class or function).
        member_type = determine_member_type(member)

        # When number is not provided parse names for suffix convention.
        if not number:
            version_re = {
                CLASS: CLASS_SUFFIX_RE,
                FUNCTION: FUNCTION_SUFFIX_RE,
            }.get(member_type)

            version = 1
            if version_re is not None:
                endswith = re.compile(version_re)
                match = endswith.search(name)

                # No match means version 1.
                if match:
                    # Get the member's base name.
                    name = name.split(match.group())[0]
                    # Get the version.
                    version = int(match.group('version'))
        else:
            # Make the number the version.
            if not isinstance(number, int):
                raise InvalidVersionException('Only integers allowed as version!')
            version = number

        # Get all versions of member name.
        version_members = version_table[name]

        # Check for duplicates.
        if version_members['members'].get(version):
            error = 'Duplicate version number `%s` for `%s` in file `%s`' % (
                version,
                name,
                module.__file__,
            )
            raise DuplicateVersionException(error)

        # Add the version as attribute for validation purposes.
        setattr(member, '__version__', version)

        # Make sure the inheritance rules are not violated for classes.
        if member_type is CLASS:
            validate_inheritance_for_class(member)

        # Get or create the proxy class to return.
        proxy = version_members.get('proxy', create_proxy_class(name))

        # Add new version method to this proxy class.
        setattr(proxy, '%s%s' % (PROXY_VERSION_TAG, version), staticmethod(member))

        # Update the version table with new versioned member/latest proxy class.
        version_members['proxy'] = proxy
        version_members['members'][version] = member
        setattr(module, '__version_table__', version_table)

        return proxy
    return wrap
