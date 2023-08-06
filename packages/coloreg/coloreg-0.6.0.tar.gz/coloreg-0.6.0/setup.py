import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.6.0'
PACKAGE_NAME = 'coloreg'
AUTHOR = 'Jacek Apanasik'
AUTHOR_EMAIL = 'jacek.apanasik@gmail.com'
URL = 'https://github.com/istot/coloreg'

LICENSE = 'MIT License'
DESCRIPTION = 'Style, sheet, theme - simple coloring for python standard `logging` module'
LONG_DESCRIPTION = (HERE / 'README.md').read_text()
LONG_DESC_TYPE = 'text/markdown'

INSTALL_REQUIRES = ['colorama']


setup(name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESC_TYPE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        url=URL,
        install_requires=INSTALL_REQUIRES,
        package_dir={'':'src'},
        py_modules = ['coloreg'],
        classifiers=[
                'Development Status :: 4 - Beta',
                'Natural Language :: English',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9'])
