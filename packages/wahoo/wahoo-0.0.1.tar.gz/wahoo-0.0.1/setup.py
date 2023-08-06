import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wahoo",
    version="0.0.1",
    author="Allan Evans",
    author_email="allan.evans@nanoporetech.com",
    description="Wahoo placeholder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nanoporetech/taiyaki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
