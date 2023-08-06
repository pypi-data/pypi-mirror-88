from http_api_client import __version__
from setuptools import setup, find_packages
from io import open
from os import path

readme = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(readme, 'r') as f:
    readme_contents = f.read()

#requirements = path.join(path.abspath(path.dirname(__file__)), 'requirements.txt')
#with open(requirements, 'r') as f:
#    install_requires = f.readlines()

setup(
  name = 'http_api_client',
  version = __version__,
  description = 'Library for HTTP Api',
  long_description = readme_contents,
  long_description_content_type = 'text/markdown',
  url = 'https://gitlab.bjarnessen.no/lib/http_client',
  author = 'Bjarne Rørnes',
  author_email = 'bjarne@bjarnessen.no',
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  keywords = 'python development library',
  packages = find_packages(),
  install_requires=['requests'],
  python_requires='>=3.6',
  project_urls={
    'Bug Reports':'https://gitlab.bjarnessen.no/lib/http_client/issues',
    'Tracker':'https://gitlab.bjarnessen.no/lib/http_client/issues',
    'Source':'https://gitlab.bjarnessen.no/lib/http_client/pylite',
  },
)
