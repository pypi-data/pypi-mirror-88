from setuptools import setup
import os

setup(name='raise_utils',
      version='1.3.1',
      description='RAISE lab package (LGPL-3.0-or-later)',
      author='RAISE, NC State University',
      author_email='ryedida@ncsu.edu',
      long_description=open(os.path.join(
          os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url='https://github.com/yrahul3910/raise',
      packages=[
          'raise_utils.data',
          'raise_utils.experiments',
          'raise_utils.hyperparams',
          'raise_utils.learners',
          'raise_utils.metrics',
          'raise_utils.transform',
          'raise_utils.transform.text',
          'raise_utils.interpret',
          'raise_utils.hooks',
          'raise_utils.utils',
          'raise_utils'
      ],
      install_requires=[
          'sklearn',
          'tensorflow',
          'keras',
          'numpy',
          'pandas',
          'cvxopt',
          'imblearn'
      ]
      )
