"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import pathlib
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    """
    Read the current version from the `_version` module.

    :return: The current version
    """
    version: Dict = {}
    exec(pathlib.Path('src/statis/_version.py').read_text(), version)
    return version['__version__']


VERSION: str = get_version()
PROJECT_URL: str = 'https://gitlab.com/BVollmerhaus/statis'
RELEASE_URL: str = (f'{PROJECT_URL}/-/archive/v{VERSION}/'
                    f'statis-v{VERSION}.tar.gz')

setup(
    name='Statis',
    version=VERSION,
    author='Benedikt Vollmerhaus',
    author_email='pypi@vollmerhaus.org',
    license='MIT',

    description='Modular system monitoring and status '
                'display via desktop notifications.',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    keywords=['status', 'system', 'info', 'monitoring',
              'notification', 'extendable', 'usability'],

    url=PROJECT_URL,
    download_url=RELEASE_URL,
    project_urls={
        'Source Code': PROJECT_URL,
        'Issue Tracker': f'{PROJECT_URL}/issues',
    },

    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['statis=statis.__main__:main']},
    python_requires='>=3.7',
    install_requires=['psutil', 'pytz'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: Desktop Environment',
        'Topic :: System :: Monitoring',
    ]
)
