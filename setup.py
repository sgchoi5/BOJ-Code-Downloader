from setuptools import setup

py_modules = [
    'requests',
    'bs4'
]

setup(name='BOJ-Code-Downloader',
      version='1.1',
      description='BOJ-Code-Downloader',
      author='Jungyeon Sohn (sjy366)',
      author_email='sjy20131565@gmail.com',
      install_requires=py_modules)