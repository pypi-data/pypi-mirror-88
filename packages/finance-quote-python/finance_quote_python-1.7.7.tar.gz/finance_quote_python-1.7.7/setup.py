"""
Setup configuration for the package.
"""
from setuptools import setup, find_packages

setup(name='finance_quote_python',
      version='1.7.7',
      description='Finance::Quote implementation in Python',
      url='https://gitlab.com/alensiljak/finance-quote-python',
      author='Alen Siljak',
      author_email='alen.siljak@gmx.com',
      license='GPL3',
      #packages=['finance_quote_python'],
      packages=find_packages(),
      zip_safe=False,
      install_requires=['requests']
      )
