import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-actions-pypi-test",
    version="1.0.0",
    author="Vaisakh Pisharody",
    author_email="vaisakh.cob@gmail.com",
    description="Just a simple Hello World package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vaisakhpisharody/python-actions-pypi-test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)