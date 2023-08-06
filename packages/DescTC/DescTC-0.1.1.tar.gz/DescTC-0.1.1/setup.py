import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DescTC",
    version="0.1.1",
    author="Mariane Alves",
    author_email="mariane.estatistica@gmail.com",
    license="MIT",
    keywords=["describe", "table", "chart"],
    description="The package includes methods that condense large amounts of information about each variable of your dataset into easy-to-understand formats (table and charts) that clearly and effectively communicate important points.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarianeAlves/DescTC",
    packages=setuptools.find_packages(include=['DescTC']),
    install_requires=[
       'pandas >= 1.1',
       'numpy >= 1.19',
       'matplotlib >= 3.3',
       'seaborn >= 0.11'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

