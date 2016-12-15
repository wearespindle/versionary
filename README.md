# Versionary

[![Build Status](https://travis-ci.org/wearespindle/versionary.svg?branch=develop)](https://travis-ci.org/wearespindle/versionary)

Package that allows to version code paths with the use of a decorator.

## Status

Currently actively used and watched.

## Usage

### Requirements

 * python 2.7
 * python 3.3, 3.4, 3.5

### Installation

Currently installing from github is the only way. Will be on PyPI in
the near future.

### Running

Usage 1.
```python

from versionary.decorators import versioned

@versioned()
def my_func():
    return 1

@versioned()
def my_func__v2:
    return 2

one = my_func.v1()
two = my_func.v2()
```

Usage 2.
```python
@versioned(1)
def my_func():
    return 1

@versioned(2)
def my_func:
    return 2

one = my_func.v1()
two = my_func.v2()
```

You can use the validate_module function from versionary.utils to
validate correct use of the decorator in the given module.


## Contributing

See the [CONTRIBUTING.md](CONTRIBUTING.md) file on how to contribute to this project.

## Contributors

See the [CONTRIBUTORS.md](CONTRIBUTORS.md) file for a list of contributors to the project.

## Roadmap

### Changelog

The changelog can be found in the [CHANGELOG.md](CHANGELOG.md) file.

### In progress

 * Minor improvements

### Future

 * Scoped versioning (Class methods)

## Get in touch with a developer

If you want to report an issue see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more info.

We will be happy to answer your other questions at opensource@wearespindle.com
