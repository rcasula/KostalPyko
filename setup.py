from setuptools import setup

setup(
    name='kostalpyko',
    version='v0.4',
    packages=['tests', 'kostalpyko'],
    install_requires=[
          'lxml',
      ],
    url='https://github.com/gieljnssns/KostalPikoPy',
    license='MIT',
    author='Giel Janssens',
    author_email='gieljnssns@vivaldi.net',
    description='A package for working with a Piko Inverter from Kostal'
)
