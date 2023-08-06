import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-jarvis", # Replace with your own username
    version="0.0.4",
    author="Philipp Scheer",
    author_email="scheer28philipp@gmail.com",
    description="Helper classes for Jarvis applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/open-jarvis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


