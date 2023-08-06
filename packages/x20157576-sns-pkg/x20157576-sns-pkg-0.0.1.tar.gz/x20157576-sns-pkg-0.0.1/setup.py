import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x20157576-sns-pkg",
    # Replace with your own username above
    version="0.0.1",
    author="x20157576",
    author_email="x20157576@student.ncirl.ie",
    description="A small boto3 send SNS text message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x20157576/cpp_ca",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=['boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)