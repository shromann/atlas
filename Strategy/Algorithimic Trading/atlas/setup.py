# setup.py

from setuptools import setup, find_packages

setup(
    name='atlas',
    version='0.1.0',
    description='a package to assist conduct quantitative research in financial market',
    author='Shromann Majumder',
    author_email='shromannmajumder@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'alpaca-trade-api',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)