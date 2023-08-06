from setuptools import setup, find_packages


setup(
    name='Py2Crawl',
    version='0.0.1.dev1',
    description='A python framework to scrape/crawl the web in an async way',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/iiestIT/PyCrawl',
    author='iiestIT',
    author_email='it.iiest.de@gmail.com',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ],
    keywords='pyside2 framework web spider async',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines()
)
