import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clarku_niulabtesting2",
    version="0.0.1",
    maintainer="Cat Mai",
    maintainer_email="CMai@clarku.edu",
    description="Example package for Youtube crawler",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)