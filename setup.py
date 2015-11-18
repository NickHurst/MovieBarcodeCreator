from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README_PyPi.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='moviebarcodecreator',
    version='0.7.3',
    description='A tool to capture frames from a video and create a barcode from it.',
    long_description=long_description,

    url='https://github.com/TheNickHurst/MovieBarcodeCreator',

    author='Nick Hurst',
    author_email='nickthurst@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='movie barcode',

    packages=['moviebarcode'],
    install_requires=['Pillow', 'setuptools'],
    entry_points={
        'console_scripts': [
            'moviebarcode = moviebarcode:main'
        ]
    }
)