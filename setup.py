# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pycmark',
    version='0.1.0',
    url='https://github.com/tk0miya/pycmark',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='CommonMark parser for docutils',
    long_description='ComomnMark parser for docutils',
    long_description_content_type='text/x-rst',
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
        'Programming Language :: Python :: 3.7',
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
