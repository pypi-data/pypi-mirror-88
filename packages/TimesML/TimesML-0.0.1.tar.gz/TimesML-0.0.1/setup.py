import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TimesML",
    version="0.0.1",
    author="leodflag",
    author_email="lovedoglion5@gmail.com",
    description="This package is used for time series data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leodflag/TimesML",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.6',
)
