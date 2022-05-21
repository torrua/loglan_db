# !/usr/bin/env python
# from distutils.core import setup
from io import open

from setuptools import setup


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(
  name='Loglan-DB',
  packages=['loglan_db'],
  package_data={'loglan_db': ['*'], },
  include_package_data=True,
  version='0.1.20',
  license='MIT',
  description="Loglan Dictionary Database Model for SQLAlchemy",
  long_description=read("README.md"),
  long_description_content_type="text/markdown",
  author='torrua',
  author_email='torrua@gmail.com',
  url='https://github.com/torrua/loglan_db',
  download_url='https://github.com/torrua/loglan_db/archive/v0.1.20.tar.gz',
  keywords=['Loglan', 'Dictionary', 'Database', 'Model', 'LOD'],
  install_requires=[
          'flask', 'sqlalchemy', 'flask_sqlalchemy', 'psycopg2',
  ],
  classifiers=[
    'Development Status :: 5 - Production',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Framework :: Flask',
    'Topic :: Database',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  python_requires='>=3.8',
)
