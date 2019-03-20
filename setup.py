from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pycmark',
    version='0.9.1',
    url='https://github.com/tk0miya/pycmark',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='CommonMark parser for docutils',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    entry_points={
        'console_scripts': [
            'md2html = pycmark.cli:md2html',
        ]
    },
    install_requires=[
        'docutils',
    ],
    extras_require={
        'test': [
            'tox',
            'flake8',
            'flake8-import-order',
            'pytest',
            'mypy',
        ],
    },
    platforms='any',
    packages=find_packages(),
)
