from setuptools import (
    setup, 
    find_packages
)

setup(
    name='ynabsearch',
    version='1.0.0',
    author='Murray Glanzer',
    packages=find_packages(),
    install_requires=[
        'click',
        'elasticsearch',
        'requests' 
    ],
    entry_points={
        'console_scripts': [
            'ynabsearch=ynabsearch.cli:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
