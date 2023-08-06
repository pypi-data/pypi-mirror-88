import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-util-hunterb9101", # Replace with your own username
    version="0.0.1",
    author="H. Boles",
    author_email="hunterb9101@gmail.com",
    description="My miscellaneous Python utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hunterb9101/Pyutil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)