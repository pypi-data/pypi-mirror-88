import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irate",
    version="0.0.1",
    author="Jon Riehl",
    author_email="jon.riehl@gmail.com",
    description="A library for doing static analysis in/on Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/operator-9/irate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
