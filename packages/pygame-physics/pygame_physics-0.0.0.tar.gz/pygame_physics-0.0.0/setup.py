from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['pygame_physics']

setup(
    name="pygame_physics",

    version="0.0.0",
    packages=packages,
    install_requires=[
        'pygame',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A way to manage physics of objects in pygame",
    long_description=long_description,
    license="PSF",
    keywords="grant miller pygame physics",
    url="https://github.com/GrantGMiller/pygame_physics",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/pygame_physics",
    }

)
