"""
How to upload new version:
1. Delete dist
2. Up the version number
3. Create dist directory using command: python setup.py sdist bdist_wheel
4. Upload using command: twine upload dist/*
"""
import pathlib
import setuptools

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='user_inputs_for_args',
    version='0.0.2',
    description="gets inputs from the user on the cmd line for params that you haven't entered programmatically",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/section.80/user_inputs_for_args',
    author='Brooklyn Germa',
    author_email='brooklyn.germa@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[],
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
)
