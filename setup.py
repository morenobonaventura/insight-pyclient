import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="insight_pyclient",
    version="0.1",
    author="Thibault de Balthasar",
    author_email="contact (@) thibaultdebalt [.] fr",
    description=("A client for Bitpay Insight API"),
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    keywords="bitpay bitcoin api",
    url="https://github.com/tdebalt/insight-pyclient",
    packages=['insight_pyclient'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ], requires=['requests']
)
