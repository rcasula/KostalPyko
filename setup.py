from setuptools import setup

setup(
    name="kostalpiko",
    version="v0.3",
    packages=["tests", "kostalpiko"],
    install_requires=["lxml",],
    url="https://github.com/rcasula/kostalpiko",
    license="MIT",
    author="Roberto Casula",
    author_email="roberto@casula.dev",
    description="A package for working with a Piko Inverter from Kostal",
)
