import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="pygiftbit",
    version="1.0.1",
    description="A simple Python wrapper for the Giftbit API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Donald Brown",
    author_email="donald.k.brown3@gmail.com",
    url="https://github.com/donaldkbrown/pygiftbit",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pygiftbit"],
    include_package_data=True,
    install_requires=["requests"]
)
