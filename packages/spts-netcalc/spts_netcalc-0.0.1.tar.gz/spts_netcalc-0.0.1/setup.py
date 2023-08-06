import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spts_netcalc", # Replace with your own username
    version="0.0.1",
    author="Santiago Soares",
    author_email="santiagosoares@gmail.com",
    description="A simple network calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)