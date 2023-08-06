import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bigbird",
    version="0.0.23",
    author="Sean Rhee",
    author_email="seanrhee2024@u.northwestern.edu",
    description="Genetic Algorithms in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s2011r2593/big-bird",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)