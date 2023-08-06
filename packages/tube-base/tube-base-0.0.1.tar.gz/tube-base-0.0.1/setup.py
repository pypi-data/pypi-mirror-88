# Standard library imports
from os import path

# Third party imports
from setuptools import (  # Always prefer setuptools over distutils
    find_packages,
    setup,
)

# Local application imports
from tube_base import __version__

here = path.abspath(path.dirname(__file__))

setup(
    name="tube-base",
    version=__version__,
    description="Base of the tube box",
    long_description="",
    url="https://github.com/sixcodes/tube-base",
    # Author details
    author="Jesué Junior",
    author_email="opensource@sixcodes.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    test_suite="tests",
    install_requires=[],
    entry_points={},
)
