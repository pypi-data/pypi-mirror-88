import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="salesvision",
    version="0.1.6",
    author="broutonlab",
    author_email="poltavsky@broutonlab.com",
    description="Salesvision provides accurate, reliable and scalable fashion image analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "imagehash",
        "numpy",
        "pymongo",
        "requests",
        "pillow",
        "opencv-python"
    ],
    python_requires='>=3.6',
)