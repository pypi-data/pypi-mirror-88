import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decopy",
    version="0.0.2",
    author="yogesh kartik",
    author_email="kartikyogesh2004@gmail.com",
    description="This is a module for decoration in python cli runtime environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yogeshkartik/decopy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)