import setuptools

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aspaceai",
    version="1.0.12",
    author="Salil Shekharan",
    author_email="salilshekharan@gmail.com",
    description="Python SDK for the ASpace AI cognitive services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.9',
)
