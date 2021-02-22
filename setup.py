import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open("caravagene/version.py").read())  # loads __version__

setup(
    name="caravagene",
    version=__version__,
    author="Zulko",
    description="",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    keywords="SBOL DNA assembly plot",
    scripts=["scripts/caravagene"],
    install_requires=["docopt", "openpyxl", "jinja2", "pandas"],
    include_package_data=True,
    packages=find_packages(exclude="docs"),
)
