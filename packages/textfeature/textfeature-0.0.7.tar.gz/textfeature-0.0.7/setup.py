import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textfeature",
    version="0.0.7",
    author="Farshad Hasanpour",
    author_email="farshad.hasanpour96@gmail.com",
    description="transform unstructured text to feature vector using word2vec, lexicon and ... ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Farshad-Hasanpour/textfeature",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)