#!/usr/bin/env python

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        ext_modules=[
            setuptools.Extension('treehouse', ['treehouse.pyx']),
        ],
    )
