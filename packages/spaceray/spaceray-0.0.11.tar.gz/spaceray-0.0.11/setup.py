"""Setup for the spaceray package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Max Zvyagin",
    author_email="max.zvyagin7@gmail.com",
    name='spaceray',
    license="MIT",
    description='Integration of HyperSpace with Ray Tune search automation.',
    version='v0.0.11',
    long_description=README,
    url='https://github.com/maxzvyagin/spaceray',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['scikit-learn==0.22.1', 'scikit-optimize==0.5.2', 'ray', "ray [tune]", "hyperspaces"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)