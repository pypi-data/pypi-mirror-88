import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pybsh",
    version="1.0.0",
    author="driazati",
    author_email="email@example.com",
    description="Use sh-style piping in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/driazati/pybsh",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)