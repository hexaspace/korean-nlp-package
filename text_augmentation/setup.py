import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sms_ner_pkg",
    version="0.0.1",
    author="hanyang2021",
    author_email="gyuree.kim.dev@gmail.com, hexa6do@gmail.com",
    description="extract location entity names from sms text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gyuree-kim/korean-nlp-package/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)