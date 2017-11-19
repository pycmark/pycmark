# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pycmark',
    version='0.1.0',
    url='https://github.com/tk0miya/pycmark',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
    ],
    install_requires=[
        'docutils',
    ],
    extras_require={
        'test': [
            'tox',
            'flake8',
            'pytest',
            'mypy',
        ],
    },
    platforms='any',
    packages=find_packages(),
)
