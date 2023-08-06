# DON'T IMPORT ANY MODULE FROM THE PACKAGE !
import setuptools


with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()


NAME = "hubstore"
VERSION = "0.0.0"
AUTHOR = "Pyrustic Evangelist"
EMAIL = "pyrustic@protonmail.com"
DESCRIPTION = "No description available"
URL = "https://github.com/pyrustic/hubstore"


setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
