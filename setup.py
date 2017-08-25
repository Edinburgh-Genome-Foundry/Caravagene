import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('caravagene/version.py').read()) # loads __version__

setup(name='caravagene',
      version=__version__,
      author='Zulko',
    description='',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords="SBOL DNA assembly plot",
    packages= find_packages(exclude='docs'))
