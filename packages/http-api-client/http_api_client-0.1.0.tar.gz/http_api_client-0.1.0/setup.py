from http_api_client import __version__
from setuptools import setup, find_packages
from io import open
from os import path

url = 'https://gitlab.bjarnessen.no/bjarne/http_api_client/'

readme = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(readme, 'r') as f:
  readme_contents = f.read()

requirements = [
  'requests',
]
  
setup(
  name = 'http_api_client',
  version = __version__,
  description = 'Library for HTTP Api',
  long_description = readme_contents,
  long_description_content_type = 'text/markdown',
  url = url,
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
  install_requires=requirements,
  python_requires='>=3.6',
  project_urls={
    'Bug Reports':f'{url}issues',
    'Tracker':f'{url}issues',
    'Source':url,
  },
)

