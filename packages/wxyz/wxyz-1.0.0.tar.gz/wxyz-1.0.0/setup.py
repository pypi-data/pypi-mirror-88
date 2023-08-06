from os.path import abspath, dirname, join
from setuptools import find_packages, setup
from wxyz.__init__ import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


setup(
    name="wxyz",
    version=__version__,
    description="a weather cli ",
    long_description=long_description,
    url="https://gitlab.com/raiyanyahya/python-cli-github-action",
    author="Raiyan Yahya",
    author_email="raiyanyahyadeveloper@gmail.com",
    keywords="cli",
    packages=find_packages(),
    install_requires=["click", "pytest"],
    extras_require={"test": ["coverage", "pytest", "pytest-cov"]},
    entry_points={"console_scripts": ["wxyz=wxyz.cli:cli"]},
    tests_require=["mock >= 2.0.0"],
)
