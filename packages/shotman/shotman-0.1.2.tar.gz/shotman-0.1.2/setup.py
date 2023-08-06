#!/usr/bin/env python3
from setuptools import setup

setup(
    name="shotman",
    description="Simple, light, modern tool for screenshooting.",
    author="Hugo Osvaldo Barrera",
    author_email="hugo@barrera.io",
    url="https://gitlab.com/whynothugo/shotman",
    license="ISC",
    packages=["shotman"],
    include_package_data=True,
    entry_points={"console_scripts": ["shotman = shotman:run"]},
    install_requires=[
        "pyside6",
    ],
    long_description=open("README.rst").read(),
    use_scm_version={
        "version_scheme": "post-release",
        "write_to": "shotman/version.py",
    },
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        # There's not `Environment ::` classifier for Linux nor Desktop applications.
        # But there's some very specific exotic environments, which is really weird.
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.9",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
)
