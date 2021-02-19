# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

import re, os, io
from setuptools import setup

version = re.search('^__version__\s*=\s*"(.*)"',
                    open('iterm_file_handler/iterm_file_handler.py').read(),
                    re.M).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="iterm_file_handler",
    packages=["iterm_file_handler"],
    install_requires=[
      'requests',
    ],
    entry_points={
        "console_scripts":
        ['itfh = iterm_file_handler.iterm_file_handler:main']
    },
    version=version,
    description="Handle default app for file in iterm",
    long_description=io.open(
        os.path.join(os.path.dirname('__file__'), 'README.md'),
        encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="pr4bh4sh",
    url="https://github.com/pr4bh4sh/iterm-file-handler",
)
