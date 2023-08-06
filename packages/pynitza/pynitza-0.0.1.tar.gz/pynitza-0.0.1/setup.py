from os import name
from setuptools import _install_setup_requires, setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Programming Language :: Python :: 3",

]

setup(
    name="pynitza",
    version="0.0.1",
    description="Restful api integration package for janitza measuring devices",
    long_description="no long description",
    long_description_content_type="text/plain",
    url="",
    author = "Julian Stremel",
    author_email="julian-stremel@t-online.de",
    license="MIT",
    classifiers=classifiers,
    keywords="janitza",
    packages=find_packages(),
    install_requires=["requests","os","logging","datetime","smtplib","email.mime.multipart","email.mime.text","pytz","time"]


)