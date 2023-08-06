from os.path import abspath, dirname, join
from setuptools import find_packages, setup
import logging, os, sys

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


def get_version():
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
    logger = logging.getLogger("setup")
    if os.path.isfile(".version"):
        with open(".version") as version_file:
            version = version_file.read().strip()
            logger.info("Got {} from .version".format(version))
            return version
    elif (
        "build" in sys.argv
        or "egg_info" in sys.argv
        or "sdist" in sys.argv
        or "bdist_wheel" in sys.argv
    ):
        version = os.environ.get("VERSION", "0.0")  # Avoid PEP 440 warning
        logger.info("Got version {} from environment".format(version))
        if "-SNAPSHOT" in version:
            version = version.replace("-SNAPSHOT", ".0")
            logger.info(
                "Replaced '-SNAPSHOT' in version with '.0', resulting in version {}".format(
                    version
                )
            )
        with open(".version", "w+") as version_file:
            version_file.write(version)
            logger.info("Wrote {} to .version".format(version))
        return version


setup(
    name="wxyz",
    version=get_version(),
    description="a weather cli ",
    long_description="this test cli was built, testes, packaged and uploaded using github actions",
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
