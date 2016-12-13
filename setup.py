from setuptools import find_packages, setup

import versionary


# Get the long description from the README file.
with open('README.md') as f:
    long_description = f.read()

install_requires = [
    'six>=1.9.0',
]

tests_require = [
    'pytest==3.0.5',
    'pytest-cov==2.4.0',
    'pytest-flake8==0.8.1',
]

setup(
    name=versionary.__title__,
    version=versionary.__version__,
    description='Code versioning decorator',
    long_description=long_description,
    url='https://github.com/wearespindle/versionary',
    author=versionary.__author__,
    author_email=versionary.__email__,
    license=versionary.__license__,
    install_requires=install_requires,
    tests_require=tests_require,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
