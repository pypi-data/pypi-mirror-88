import os
from distutils.core import setup


def version():
    setupDir = os.path.dirname(os.path.realpath(__file__))
    versionFile = open(os.path.join(setupDir, 'gtdb_validation_tk', 'VERSION'))
    return versionFile.readline().strip()


setup(
    name='gtdb_validation_tk',
    version=version(),
    author='Donovan Parks',
    author_email='donovan.parks@gmail.com',
    packages=['gtdb_validation_tk'],
    package_data={'gtdb_validation_tk': ['VERSION']},
    entry_points={
        'console_scripts': [
            'gtdb_validation_tk = gtdb_validation_tk.__main__:main'
        ]
    },
    url='https://pypi.org/project/gtdb-validation-tk/',
    license='GPL3',
    description='A toolbox for validating the GTDB taxonomy.',
    install_requires=[
        "numpy >= 1.8.0",
        "biolib >= 0.1.6",
        "dendropy >= 4.0.0",
        'fuzzywuzzy'],
)
