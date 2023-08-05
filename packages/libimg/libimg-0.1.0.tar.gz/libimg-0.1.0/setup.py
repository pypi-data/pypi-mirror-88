from distutils.core import setup
from setuptools import find_packages
setup(name='libimg',
      version='0.1.0',
      description='Library code for image processing',
      author='Matthew McRaven',
      author_email='mkm302@georgetown.edu',
      packages=find_packages('src'),
      package_dir={'': 'src'},
     )