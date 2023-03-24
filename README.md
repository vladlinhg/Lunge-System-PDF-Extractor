# Lunge-System-PDF-Extractor 
    This is an application that extracts the contents of pdf files into string format; the resulting extracted data will then be stored into a json file, which can be extracted to a mySQL database
# Developer Team
    Nai Yen Lin
    Eddie Wang
# Installation & Environment
1. install pdfplumber
    1. pip install pdfplumber
    2. pip install tqdm (progress bar for directory scan)
    3. pip install nltk 


# Features to be Implemented
1. Directory Record
    1. Goals
        1. Store path, name, tag, etc.
        2. Data stored in json/csv/txt
        3. Directory class
        4. Flask app/GUI (not sure if we will get this done)
    2. Progress
        1. Directory class established
        2. Data stored in .json
        3. Metadata is now stored in .json

2. Read Function
    1. Goal
        1. Original plan: use pdfminer (not ideal as it stopped being maintained from 2020) / new plan: use pdfPlumber (still in DevOps)
        2. Output pdf content into dictionary, and then to a json file
    2. Progress
        1. Can read multiple pdfs, seperates the paragraphs and appends to a dictionary with the relevant metadata.
        2. Has the option to get output from a single pdf, or from an entire directory. 
    3. Comparison

| Product      | Speed       | Text Extract | Table Extract | External Library | In DevOps |
| -----------  | ----------- | ------------ | ------------- | ---------------- | --------- |         
| pdfminer     | Fast        | Yes          | No            | No               | No        |
| PyPDF2       | Moderate    | Yes          | No            | No               | No        |
| pymupdf      | Fastest     | Yes          | No            | Needed           | Yes       |
| tabula-py    | Moderate    | No           | Yes           | No               | No        |
| pdfPlumber   | Fast        | Yes          | Yes           | No               | Yes       |     

3. Output Function
    1. Goal
        1. Dictionary will be output into json files stored into specific directory appointed by user
        2. Make sure metadata is there for smooth implementation into mySQL database
    2. Progress
        1. Output format is json file (most likely will not change)
        2. Output directory can selected, metadata is there and the implementation to the mySQL database seems smooth (testing)
