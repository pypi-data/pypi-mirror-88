import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="queryparams-liberdade",
    version="0.0.1",
    author="Cristiano Silva Jr",
    author_email="crisjr@pm.me",
    description="Objects as query parameters",
    long_description="Parse query parameters as objects to be used in Python",
    long_description_content_type="text/markdown",
    url="https://github.com/liberdade-organizacao/queryparams",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
