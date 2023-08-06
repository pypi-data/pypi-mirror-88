# This file is if we want to be able to pip install it & upload the package to pypi

from setuptools import setup

setup(name='ds_functions_pkg',
      version='0.3.0',
      description='useful data science functions',
      author='Taylor Martin',
      author_email='taymart@gmail.com',
      url='https://github.com/taylor-m/ds_functions_pkg',
      packages=['functions_pkg'],
      license='MIT',
      )
