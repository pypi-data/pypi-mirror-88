from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wiz-utils',

    version='1.0.2',

    description='wiz-utils',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://chnyangjie.github.io/',

    author='chnyangjie',

    author_email='chnyangjie@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='utils string array',
    package_dir={'wiz_utils': 'src/wiz_utils'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=[''],
    py_modules=['wiz_utils'],
    project_urls={
        'Bug Reports': 'https://github.com/chnyangjie/wiz_utils/issues',
        'Say Thanks!': 'https://github.com/chnyangjie/wiz_utils/issues',
        'Source': 'https://github.com/chnyangjie/wiz_utils',
    },
)
