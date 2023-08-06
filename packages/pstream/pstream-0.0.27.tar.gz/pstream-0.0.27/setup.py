import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pstream",
    version="0.0.27",
    author="Christopher Henderson",
    author_email="chris@chenderson.org",
    description="Provides a Stream and AsyncStream for composing fluent lazily evaluated, sync/async fusion, iterators.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christopher-henderson/pstream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["future>=0.18.2"],
    python_requires=' >=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
)
