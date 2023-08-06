import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Reference from https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="gmtk",
    version="0.0.1",
    author="Michael Hoffman",
    author_email="michael.hoffman@utoronto.ca",
    description="Python interface for handling Graphical Models Toolkit markup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoffmangroup/gmtk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)