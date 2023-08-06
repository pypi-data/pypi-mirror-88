import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfacegen",
    version="0.1.8",
    author="Jack Saunders",
    author_email="jrs68@bath.ac.uk",
    description="A mesh library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jsaunders909/PyFaceGen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
