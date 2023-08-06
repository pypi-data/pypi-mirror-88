import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="common-harness-lib",
    version="0.0.15",
    author="Highway to HAL",
    author_email="h2h@georgeom.net",
    description="Helper package for H2H Task images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2hal/common-harness-lib",
    packages=setuptools.find_packages(),
    install_requires=[
        "boto3",
        "botocore"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
