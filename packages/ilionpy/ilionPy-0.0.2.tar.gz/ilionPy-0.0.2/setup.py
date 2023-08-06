import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ilionPy", 
    version = "0.0.2", 
    author = "Peter Gross", 
    author_email = "peter@ilion.co.za", 
    description = "Ilion Function Library", 
    long_description = long_description, 
    long_description_content_type="text/markdown", 
    url="http://www.ilionanalytics.com", 
    packages=setuptools.find_packages(), 
    classifiers = [
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent", 
    ],
    python_requires = ">=3.6",
)