#!/usr/bin/env python
import re
from io import open
from setuptools import setup

version_file = open('quantum_core/__init__.py', encoding='utf8')
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                          version_file.read(), re.M)
version_file.close()
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

setup(
    version=version,
)
