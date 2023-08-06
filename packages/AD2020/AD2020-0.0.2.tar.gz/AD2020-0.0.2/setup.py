import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AD2020",
    version="0.0.2",
    author="Yuxi Liu, Zhufeng Kang, Esther Brown",
    author_email="yuxiliu@mail.harvard.edu, zhk877@g.harvard.edu, estherbrown@g.harvard.edu",
    description="An automatic differentiation package",
    long_description="AD2020 is a Python package for automatic differentiation (AD). Differentiation is one of the key components in numerical computing and is ubiquitous in machine learning, optimization, and numerical methods. By repeatedly applying chain rule to elementary arithmetic operations and functions, AD is powerful to efficiently compute derivatives for complicated functions to machine precision.",
    long_description_content_type="text/markdown",
    url="https://github.com/ZLYEPJ20/cs107-FinalProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
