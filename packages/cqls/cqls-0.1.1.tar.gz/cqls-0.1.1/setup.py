from setuptools import setup

setup(name='cqls',
      version='0.1.1',
      description='A parser for an often-used subset of CQL',
      url='http://github.com/liao961120/cqls',
      author='Yongfu Liao',
      author_email='liao961120@github.com',
      license='MIT',
      packages=['cqls'],
      tests_require=['deepdiff'],
      zip_safe=False)