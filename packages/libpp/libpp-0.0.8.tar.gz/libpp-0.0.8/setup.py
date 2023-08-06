import os
import re
import sys

from setuptools import setup, find_packages


setup(
    name='libpp',
    version='0.0.8',
    description="peng's python library",
    author='hupeng,zhangpeng',
    author_email='hupeng@webprague.com',
    python_requires=">=3.5",
    url='https://github.com/chmod740/libpp',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['numpy>=1.0.2', 
                      'scipy>=1.0.0'],
    license='Apache License 2.0',
    zip_safe=False,
)
