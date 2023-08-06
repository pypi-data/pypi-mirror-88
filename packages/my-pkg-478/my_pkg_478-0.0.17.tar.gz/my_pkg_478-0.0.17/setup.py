from setuptools import setup
import versioneer

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="my_pkg_478",
    version=versioneer.get_version(),
    description="My package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Curtis Hampton",
    author_email="CurtLHampton@gmail.com",
    url="https://github.com/CurtLH/my_pkg",
    packages=["my_pkg"],
    install_requires=requirements,
    entry_points={"console_scripts": ["my_pkg=my_pkg.cli:my_pkg"]},
    extras_require={"dev": ["pytest", "sphinx"]},
    keywords="my_pkg",
    classifiers=["Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7"],
)
