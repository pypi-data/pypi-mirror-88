import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tingkartapi", 
    version="1.0.7",
    author="Didrik Schønberg, Per Helge Litzheim Frøiland, Thomas Heggelund",
    author_email="didrikfs@live.no",
    description="Tingkart api installation package",
    long_description="Tingkart API",
    long_description_content_type="text/markdown",
    url="https://github.com/577799/Tingkart_api",
    py_modules=["tingkart_api"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)