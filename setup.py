#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "pytest>=3.6.0",
        "pytest-ethereum>=0.1.3a6,<1",
        "pytest-xdist",
        "tox>=2.9.1,<3",
    ],
    'lint': [
        "black>=18.6b4,<19",
        "flake8==3.4.1",
        "isort>=4.2.15,<5",
        "mypy<0.600",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint'] +
    extras_require['doc']
)

setup(
    name='twig',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.1.0-alpha.5',
    description="""twig: A tool for Ethereum smart contract development.""",
    long_description_markdown_filename='README.md',
    author='Nick Gheorghita',
    author_email='nickg@ethereum.org',
    url='https://github.com/ethereum/twig',
    include_package_data=True,
    install_requires=[
        "eth-utils>=1.4.1,<2",
        "ethpm>=0.1.4a10,<1",
        "web3[tester]>=5.0.0a3,<6",
        "vyper>=0.1.0b6,<1",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['twig'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
