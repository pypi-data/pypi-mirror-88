import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as fh:
    long_description = fh.read()

setuptools.setup(
    name="scam",
    version="0.3.9", 
    author="Codalyzers",
    author_email="djoni.austin@gmail.com",
    description="Source Code Analyzing Maching is an application for the analysis of similarities between source code files. Currently with Python, Java, C, and C++ file checking capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SourceCodeAnalyzingMachine/SCAM_Public",
#    package_dir={"": "source"},
    packages=setuptools.find_packages(), #where='source'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['javalang', 'PySide2', 'matplotlib','networkx','clang', 'pycparser', 'grave'],
    include_package_data=True,
    package_data={
        "": [ "*.txt","*.py","*.png", "source/*.py","source/backend/*.py","source/frontend/*.py",
        "source/frontend/*.png","source/frontend/gui/*.ui","source/frontend/pages/*.py","source/frontend/util/*.py"],
    },
    entry_points={
        'console_scripts': [
            'source_analyzer=source.scam:main',
            'source-analyzer=source.scam:main',
            'scam=source.scam:main',
        ],
    },
)
