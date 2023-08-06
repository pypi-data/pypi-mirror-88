import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()


setuptools.setup(
    name="Logger.py",
    version="1.0.0",
    author="NullPointer",
    author_mail="nicopatermann007@gmail.com",
    description="This is a Logger package. With this package can you log things.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/NullPointer-Nico/Logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)