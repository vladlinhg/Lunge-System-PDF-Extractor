# Lunge-System-PDF-Extractor 
    This is an application that extracts the contents of pdf files into string format; the resulting extracted data will then be stored into either a MySQL DB, json, or other file extension.
# Developer Team
    Nai Yen Lin
    Eddie Wang
# Installation & Environment
1. install pdfplumber
    1. pip install pdfplumber
    2. pip install tqdm (progress bar for directory scan)


# Features to be Implemented
1. Directory Record
    1. Goal 
        1. Store path, name, tag, etc.
        2. Data stored in json/csv/txt
        3. Directory class
    2. Progress
        1. Directory class established
        2. Data stored in .json

2. Read Function
    1. Goal
        1. Original: pdfminer (stop maintained from 2020) / new: pdfPlumber (still in DevOps)
        2. Output pdf content into dictionary
    2. Progress
        1. Can read multiple pdfs, seperates the paragraphs into a list.
        2. Option to get output from a single pdf, or from an entire directory. 
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
        1. dictionary will be output into json files stored into specific directory appointed by user
        2. MySQL table has limit on text length
    2. Progress
        1. Output format is json file
        2. Output directory can be appointed 
