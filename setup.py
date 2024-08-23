#!/usr/bin/env python
import io

from setuptools import setup, find_packages
from distutils.util import convert_path

PROJECT = "evalai"
package_config = {}
version_file_path = convert_path("evalai/version.py")

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(version_file_path) as version_file:
    exec(version_file.read(), package_config)

tests_require = [
    "coverage",
    "coveralls==1.3.0",
    "flake8==3.0.4",
    "pytest==3.5.1",
    "pytest-cov==2.5.1",
    "pytest-env==0.6.2",
    "responses==0.9.0",
    "pre-commit==1.14.4",
]

setup(
    name=PROJECT,
    version=package_config["__version__"],
    description="Use EvalAI through command line interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cloud-CV",
    author_email="team@cloudcv.org",
    url="https://github.com/Cloud-CV/evalai_cli ",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
    platforms=["Any"],
    scripts=[],
    provides=[],
    install_requires=requirements,
    tests_require=tests_require,
    namespace_packages=[],
    packages=find_packages(exclude=("docs", "scripts", "tests")),
    include_package_data=True,
    entry_points={"console_scripts": ["evalai=evalai.main:main"]},
    zip_safe=False,
)
