from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aoc-tools-dannyboywoop",
    version="1.0",
    author="Daniel Holmes",
    author_email="DanielJHolmes@hotmail.co.uk",
    description="AdventOfCode tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dannyboywoop/AOC_Tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)