import setuptools

long_description = open('README.md').read()

setuptools.setup(
    name="pyhs3",
    version="0.14",
    author="Mark Coombes",
    author_email="mark@markcoombes.ca",
    description="Python3 async library for interacting with HomeSeer HS3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marthoc/pyhs3",
    packages=['pyhs3'],
    install_requires=['asyncio', 'aiohttp'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
