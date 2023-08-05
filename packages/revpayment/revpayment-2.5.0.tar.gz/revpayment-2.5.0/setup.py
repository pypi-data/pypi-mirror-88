from distutils.core import setup
from revpayment import __version__
from setuptools import find_packages

setup(
    name='revpayment',
    version=__version__,
    license='MIT',
    description='payment service for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    url='https://github.com/revtel/revpayment',
    keywords=['revteltech', 'payment'],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
        'pyjwt',
        'jwcrypto'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
