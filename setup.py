from setuptools import find_packages, setup

import versionary


# Get the long description from the README file.
# For upload to pypi convert readme to rst.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ''


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
    extras_require={
        'test': tests_require,
    },
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    keyword='versioning version versioned',
    classifiers=[
        # Status.
        'Development Status :: 3 - Alpha',

        # Audience.
        'Intended Audience :: Developers',

        # License.
        'License :: OSI Approved :: MIT License',

        # Programming languages.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        # Topic.
        'Topic :: Software Development :: Version Control',
    ],

)
