import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bruhapy", # Replace with your own username
    version="2020.12.13",
    author="mikey",
    author_email="mikey@mikeyo.ml",
    description="An API wrapper for https://bruhapi.xyz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isigebengu-mikey/bruhapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)