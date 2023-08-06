#from distutils.core import setup
from setuptools import setup
setup(
  name = 'xml2df',
  packages = ['xml2df'],
  version = '0.14',
  license='Apache-2.0',
  description = 'Convert XML file to a pandas dataframe. This package flattens the XML structure and creates a list of dictionaries that is then transformed to a dataframe.',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  author = 'A. Adiby',
  author_email = 'aliadiby@gmail.com',
  url = 'https://github.com/aadiby/xml2df.git',
  download_url = 'https://github.com/aadiby/xml2df/archive/0.14.tar.gz',
  keywords = ['XML', 'DataFrame', 'DF', 'pandas', 'flat', 'ETL'],
  install_requires=[
          'validators',
          'pandas',
          'numpy',
          'python-dateutil',
          'pytz',
          'six',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.7',
  ],
)