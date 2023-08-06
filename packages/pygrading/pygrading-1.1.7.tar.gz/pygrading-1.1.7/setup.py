'''
    Name: setup.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Setup script for pygrading!
    Coding: UTF-8
'''

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

import setuptools

from pygrading import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygrading',
    version=__version__,
    author='Charles Zhang',
    author_email='694556046@qq.com',
    description='A Python ToolBox for CourseGrading platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.educg.net/zhangmingyuan/PyGrading',
    packages=['pygrading'],
    package_data={
        'pygrading': [
            'static/.gitignore',
            'static/*',
            'static/kernel/*',
            'static/kernel/templates/*',
            'static/kernel/templates/html/*',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
        'Jinja2>=2.11.2',
        'fire>=0.3.1'
    ],
)
