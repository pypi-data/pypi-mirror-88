import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="puli", 
    version="0.0.1",
    author="Prajwel Joseph",
    author_email="prajwel.joseph@gmail.com",
    description="Analyze UVIT L1 data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prajwel/puli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['numpy',
                      'astropy'],
)
