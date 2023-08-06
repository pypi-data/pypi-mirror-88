import setuptools
from pathlib import Path

setuptools.setup(
    name="package_exists",
    version="0.1.2",
    description="Check whether a package name already exists or not in Pypi repository.",
    long_description=Path("README.md").read_text(),
    url="https://pypi.org/project/package-exists/",
    author="Daniel Diaz",
    author_email="",
    license="GNU GPLv3",
    packages=setuptools.find_packages(exclude=["tests", "data"]
                                      )
)
