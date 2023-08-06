import glob
from os import path
import collections
import setuptools

MY_DIR = path.abspath(path.dirname(__file__))
with open(path.join(MY_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='horkos-doc',
    version='0.0.7',
    description=(
        'A library for building data documentation.'
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',
    url='https://gitlab.com/kjschiroo/horkos-doc',
    entry_points = {
        'console_scripts': ['horkos-doc=horkos_doc._cmdline:main'],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4', 'bleach', 'jinja2', 'markdown', 'horkos'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    package_data={'': list(glob.iglob('horkos_doc/templates/*'))},
    include_package_data=True,
)
