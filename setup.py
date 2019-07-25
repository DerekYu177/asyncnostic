import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncnostic",
    version="0.1.0",
    author="Derek Yu",
    author_email="derek-nis@hotmail.com",
    description="simple way of using pytest with async unit tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DerekYu177/asyncnostic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Framework :: AsyncIO",
    ],
)
