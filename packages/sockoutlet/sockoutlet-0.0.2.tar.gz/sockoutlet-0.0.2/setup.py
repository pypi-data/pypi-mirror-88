#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'sockoutlet',
  version = '0.0.2',
  description = 'Public URLs for testing your chatbot',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/skelethon/sockoutlet',
  download_url = 'https://github.com/skelethon/sockoutlet/downloads',
  keywords = ['proxy', 'tunnel', 'testing'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
