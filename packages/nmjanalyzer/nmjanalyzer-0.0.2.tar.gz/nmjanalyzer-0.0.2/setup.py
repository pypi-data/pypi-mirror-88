import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nmjanalyzer", # Replace with your own username
    version="0.0.2",
    entry_points = {
        "console_scripts": ['nmj_analyzer = nmj_analyzer.nmj_analyzer:main']
        },
    author="Carole Sudre",
    author_email="c.sudre@ucl.ac.uk",
    description="NMJ Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csudre/NMJ_Analyser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
