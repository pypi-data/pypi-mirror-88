import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="df2obs",
    version="0.1.0",
    description="A tool to convert DataFrame to a list of objects of some class or vice versa",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ldmax/df2obs.git",
    author="Dan Li",
    author_email="lidanmax@163.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["df2obs"],
    include_package_data=True,
    install_requires=["pandas"]
)