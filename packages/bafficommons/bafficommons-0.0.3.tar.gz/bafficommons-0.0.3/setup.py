import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bafficommons",
    version="0.0.3",
    author="Miguel Alfaro",
    author_email="malfaro@fi.uba.ar",
    description="Baffi Commons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baf-fi/baffi-commons",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)