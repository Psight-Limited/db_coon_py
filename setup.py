from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.2"
DESCRIPTION = "A simple python package to connect to our database"
LONG_DESCRIPTION = "A simple python package to connect to our database"

setup(
    name="db_con_py",
    version=VERSION,
    author="Fib",
    author_email="<Noah@psight.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license_files="LICENSE",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/Psight-Limited/db_con_py",
    keywords=["python"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
