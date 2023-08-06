import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bank Package - Aamir and Conrad", # Replace with your own username
    version="0.0.1",
    author="Aamir Khan & Conrad Yeung",
    author_email="author@example.com",
    description="This package can be used to manage bank customers (accounts and cards).",
    long_description="This package can be used to manage bank customers. There are two subpackages accounts and cards. Accounts subpackage is for corporate customers using bank for large transactions. Cards subpackage is for retail customers who would like to use their bank account with card transactions.",
    long_description_content_type="text/markdown",
    url="https://github.com/Conrad-Yeung/Data-533-Lab-4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)