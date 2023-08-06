import io
import os
import re

from setuptools import find_packages, setup

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read("README.rst")


project_urls = {
  'Docs': 'https://github.com/valhuber/logicbankutils/wiki'
}

setup(
    name="logicbankutils",
    version="0.6.0",
    url="https://github.com/valhuber/logicbankutils",
    license="BSD",
    author="Val Huber",
    author_email="valjhuber@gmail.com",
    project_urls=project_urls,
    description=(
        "Utility functions for LogicBase"
    ),
    long_description=desc(),
    long_description_content_type="text/x-rst",
    packages=['logic_bank_utils'],
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires="~=3.8"
)