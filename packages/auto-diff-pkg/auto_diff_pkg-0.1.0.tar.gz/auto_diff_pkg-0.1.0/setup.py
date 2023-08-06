import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto_diff_pkg",
    version="0.1.0",
    author="DeriveMeCrazy-AutoDiff Group 21",
    author_email="jalling@g.harvard.edu, mod821@g.harvard.edu, tliu@g.harvard.edu, alk264@g.harvard.edu",
    description="A package for performing automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeriveMeCrazy-AutoDiff/cs107-FinalProject/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['numpy>=1.19.4',
                      'pytest>=6.1.2',
                      'notebook>=6.1.5',]
)
