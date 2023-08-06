import os
from setuptools import setup, find_packages

from condition import __version__ as v

version = os.getenv("MODULE_VERSION_ID", v)

install_requires_list = open("requirements.txt").read().splitlines()
install_requires_list_dev = open("requirements-test.txt").read().splitlines()
pkgs = find_packages(".", exclude=["test/**"])
extras = {"sql": ["jinja2"], "dev": install_requires_list_dev}
extras["all_extras"] = sum(extras.values(), [])

setup(
    name="condition",
    description="A pythonic way to construct conditions for pandas dataframe query and sql",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    version=version,
    author="Weiyang Zhao",
    author_email="wyzhao@gmail.com",
    packages=pkgs,
    url="https://gitlab.com/wyzhao/condition",
    install_requires=install_requires_list,
    extras_require=extras,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    project_urls={
        "Docs": "https://condition.readthedocs.io/en/latest/",
        "Source": "https://gitlab.com/wyzhao/condition",
        "Bug Reports/Issues": "https://gitlab.com/wyzhao/condition/issues",
    },
)
