import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="msr-by-sooz",
    version="1.0.0",
    author="sooz",
    author_email="smeyer101@mac.com",
    description="a CLI for measuring things on web pages!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=["src/msr.py"],
    install_requires=[
        "argparse",
        "validator_collection",
        "requests",
        "texttable",
        "tldextract",
        "tabulate"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
