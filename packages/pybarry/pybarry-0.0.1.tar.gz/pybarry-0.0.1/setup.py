import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pybarry",
    version="0.0.1",
    description="Barry Electricity Price Consumption Data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/getbarry/pybarry",
    author="Barry",
    author_email="yash.khatri@barry.energy",
    license="MIT",
    packages=["pybarry"],
    include_package_data=True,
    install_requires=["requests"],
    platforms=["any"],
)
