import os
from setuptools import setup, find_packages

from asencis import __version__ as pkg_version, __author__ as pkg_author, __license__ as pkg_license

# Load the README file for use in the long description
local_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(local_dir, "README.md"), encoding="utf-8") as f:
  long_description = f.read()

requires = [
  "requests",
]

tests_requires = [
  "nose2",
  "nose2[coverage_plugin]",
]

extras_require = {
  "doc": ["sphinx", "sphinx_rtd_theme"],
  "test": tests_requires,
  "lint": ["pylint"],
}

setup(
    name="asencis",
    version=pkg_version,
    description="asencis Python driver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asencis/asencis-python",
    project_urls={
        "Bug Tracker": "https://github.com/asencis/asencis-python/issues",
        "Documentation": "https://asencis.com/documentation",
        "Source Code": "https://github.com/asencis/asencis-python",
    },
    author=pkg_author,
    author_email="priority@asencis.com",
    license=pkg_license,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    keywords="asencis",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=requires,
    extras_require=extras_require,
    tests_require=tests_requires,
    test_suite="nose2.collector.collector",
)
