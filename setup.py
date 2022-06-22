"""
Apple Test Log Visulation Tool

Haoxuan Zhu <hxzhu@umich.edu>
"""

from setuptools import setup

setup(
    name='datapreprocess',
    version='0.0.1',
    packages=['datapreprocess'],
    include_package_data=True,
    install_requires=[
        'click==7.0',
        'matplotlib==3.1.0',
        'numpy==1.22.0',
        
    ],
    entry_points={
        'console_scripts': [
            'datapreprocess = datapreprocess.__main__:main'
        ]
    },
)
