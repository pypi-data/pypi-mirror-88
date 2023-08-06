from setuptools import setup, find_packages
import versioneer

from pathlib import Path

here = Path(__file__).resolve().parent
long_description = here.joinpath('README.md').read_text()

setup(
    name='acondbs',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A GraphQL server for product DB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Simons Observatory',
    author_email='so_software@simonsobservatory.org',
    url='https://github.com/simonsobs/acondbs',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=[
        'Flask>=1.1',
        'Flask-Cors>=3.0',
        'Flask-GraphQL>=2.0',
        'Flask-Migrate>=2.5',
        'Flask-SQLAlchemy>=2.4',
        'graphene-sqlalchemy>=2.3',
        'graphene-sqlalchemy-filter>=1.10',
        'SQLAlchemy-Utils>=0.36',
        'cryptography>=3.2',
        'gitpython>=3.1',
        'requests>=2.24'
    ],
    extras_require={
        'tests': [
            'pytest>=5.4',
            'pytest-cov>=2.8',
            'snapshottest>0.5'
        ]
    }
)
