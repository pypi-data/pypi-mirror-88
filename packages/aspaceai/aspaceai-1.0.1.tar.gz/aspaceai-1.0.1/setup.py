import setuptools

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aspaceai",
    version="1.0.1",
    author="Salil Shekharan",
    author_email="salilshekharan@gmail.com",
    description="Python SDK for the ASpace AI cognitive services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salilshekharan/ASpaceAI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
