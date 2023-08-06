# Source Code Analyzing Machine

[GitHub Repo Link](https://github.com/SourceCodeAnalyzingMachine/SCAM_Public)

- A locally run application that demonstrates different matching algorithms 
- Current release compares files as a one to one connection
- Outputs given percentage of similarity and highlighted visualization of the matching sections of input documents
- Supports C, C++, Java, and Python files

## Getting Started

Install PySide2: `pip install scam`

Run from directly outside `source` directory: `python3 ./source/scam.py`

## Getting Started

#### STEP 1 

it is recommended to create and navigate to virtual environemnt using python to run script

    python3.8 -m venv <dir> 
    source <dir>/bin/activate

#### STEP 2

install source_analyzer python package from Python Package Index.
**Note:** must be running python version 3.8 or greater

    pip install scam


###### OR

Download the latest built compressed file release from [source_analyzer-X.X.X.tar.gz](https://github.com/SourceCodeAnalyzingMachine/SCAM_Public/tree/master/dist)



then install downloaded file

    pip3 install /<path_to_file>/scam-0.0.2.tar.gz


#### STEP 3
(make sure xlaunch is running)
run script

    scam

## Known Errors/Issues
Issues- 
Python files featuring a heavy amount of print statements may cause skewed data. 


## Project Group: Codalyzers
- Djoni Austin | @dcaust1n
- Jared Dawson | @lukinator1
- Shane Eising | @seising99
- Julian Marott | @jmmoratta

## References: 
https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf

