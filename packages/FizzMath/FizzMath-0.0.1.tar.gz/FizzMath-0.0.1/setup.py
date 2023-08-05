import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FizzMath",
    version="0.0.1",
    author="Chee Fan",
    author_email="fizz.job@gmail.com",
    description="A testing lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fizz-whu/FizzMath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
