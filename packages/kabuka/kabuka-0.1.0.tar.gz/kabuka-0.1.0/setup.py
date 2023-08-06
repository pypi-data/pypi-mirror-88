# from distutils.core import setup
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='kabuka',
    packages=['kabuka'],
    version='0.1.0',
    license='MIT',
    description='get latest stock price from Yahoo! Finance',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Danaipat Sodkomkham',
    author_email='sdanaipat@gmail.com',
    url='https://github.com/sdanaipat/kabuka',
    download_url='https://github.com/sdanaipat/kabuka/archive/v0.1.0.tar.gz',
    keywords=['stock price', 'yahoo finance', 'market price', 'get latest stock price'],
    scripts=['./kabuka/kabuka'],
    install_requires=[
        'requests',
        'fire',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
