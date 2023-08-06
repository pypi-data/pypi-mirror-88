# has been cutomized for use in Scraper_Package

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Scraper_Package_DSC", # Replace with your own username
    version="0.0.1",
    author="Data Science Center",
    #author_email="author@example.com",
    description="News scraper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Science-Intelligence-Center/Scraper_Package.gi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
