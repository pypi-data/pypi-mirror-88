import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="myassistant",
    version="1.0.3",
    description="It is a assistant creater module :)",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Govind Potdar",
    author_email="govindpotdar2001@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["myassistant"],
    include_package_data=True,
    install_requires=["speechrecognition","pyttsx3","datetime","psutil","wikipedia","requests","prettytable","sounddevice","wavio","scipy"],
    
)