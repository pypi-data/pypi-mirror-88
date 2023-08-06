import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arabic-text-quote",  # Replace with your own username
    version="0.0.1",
    author="Abdullah Al-Aidrous",
    author_email="abdullah.alidrous@gmail.com",
    description="A package to discover texts extracted from Arabic books",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdullh-alidrous/arabic-text-quotation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
