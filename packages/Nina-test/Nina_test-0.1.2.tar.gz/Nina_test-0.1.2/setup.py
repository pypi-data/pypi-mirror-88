from setuptools import setup

__project__ = "Nina_test"
__version__ = "0.1.2"
__description__ = "A Python test module."
__packages__ = ["Nina_test"]
__author__ = "Hrishikesh Arun"
__author_email__ = "hrishikesh28arun@gmail.com"
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["learning"]
__requires__ = ["pandas"]
long_description="A Python test module that helps create .csv files and sets an app's version.(Actually it don't really sets an app's version, it prints the app appended with its version on the screen)"

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    requires = __requires__,
    long_description=long_description
    )
