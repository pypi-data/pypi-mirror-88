import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="victor-services-splitter",
    version="0.1.1",
    author="Ailab",
    author_email="ailabunb@gmail.com",
    description="Model to automatize the separation of a messy "
                "PDF into multiple documents for the Brazilian "
                "Federal Supreme Court.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gpam/victor/SERVICES/splitter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'tensorflow == 2.3.1',
        'pillow',
        'numpy'
    ],
    test_requires=[
        'pandas',
        'pyarrow'
    ],
    python_requires='>=3.6',
)
