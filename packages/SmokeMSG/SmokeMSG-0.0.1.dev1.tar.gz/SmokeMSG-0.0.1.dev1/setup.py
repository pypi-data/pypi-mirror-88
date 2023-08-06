# -*- coding: utf-8 -*-
#!/usr/bin/env python
import re
from io import open
from setuptools import setup, find_packages
from os.path import abspath, dirname, join

here = abspath(dirname(__file__))
version_file = open(join(here, 'smokemsg', '__init__.py'), encoding='utf8')
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                          version_file.read(), re.M)
version_file.close()
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

# Get the long description from the README file
long_description = open(join(here, 'README.md'), encoding='utf8').read()

setup(
    name='SmokeMSG',
    version=version,
    description='Lightweight Python library to show simple dialogs.',
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    url='https://quantumgui.github.io/smokemsg',
    author='Kavindu Santhusa',
    author_email='kavindusanthusa@gmail.com',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    keywords='dialog, popup, module, pure-python, lightweight, cross-platform, alert, prompt, confirm, question, info, ask',
    packages=['smokemsg'],
    project_urls={
        'Bug Reports': 'https://github.com/quantumgui/smokemsg/issues',
        'Source': 'https://github.com/quantumgui/smokemsg/',
    },
)
