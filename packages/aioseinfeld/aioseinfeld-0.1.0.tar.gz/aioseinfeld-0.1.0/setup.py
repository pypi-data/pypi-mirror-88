#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['aioseinfeld', 'aioseinfeld.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite']

setup(name='aioseinfeld',
      version='0.1.0',
      description="What's the deal with asyncio?",
      author='John Reese',
      author_email='john@noswap.com',
      url='https://github.com/jreese/aioseinfeld',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      python_requires='>=3.6',
     )
