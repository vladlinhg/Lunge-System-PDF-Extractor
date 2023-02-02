# Lunge-System-PDF-Extractor 
    It's an application extracting contents of pdf files into string format, and the extracted data will be stored into MySQL, json, or txt files
# Developer Team
    Nai Yen Lin
    Eddie Wang
# Installation & Environment


# Features to be Implemented
1. Database Record
    1. Goal
        1. Store host, user, password, database, table, etc.
        2. Data stored in json/csv/txt
        3. Databse class
    2. Progress
        1. Class created
        2. Connector established

2. Directory Record
    1. Goal 
        1. Store path, name, tag, etc.
        2. Data stored in json/csv/txt
        3. Directory class
    2. Progress
        1. in progress

3. Read Function
    1. Goal
        1. Original: pdfminer (stop maintained from 2020) / new: pdfPlumber (still in DevOps)
        2. Output pdf content into dictionary
    2. Progress
        1. in progress
    3. Comparison

| Product      | Speed       | Text Extract | Table Extract | External Library | In DevOps |
| -----------  | ----------- | ------------ | ------------- | ---------------- | --------- |         
| pdfminer     | Fast        | Yes          | No            | No               | No        |
| PyPDF2       | Moderate    | Yes          | No            | No               | No        |
| pymupdf      | Fastest     | Yes          | No            | Needed           | Yes       |
| tabula-py    | Moderate    | No           | Yes           | No               | No        |
| pdfPlumber   | Fast        | Yes          | Yes           | No               | Yes       |     

4. Output Function
    1. Goal
        1. dictionary will be output into json files stored into specific directory appointed by user
        2. MySQL table has limit on text length
    2. Progress
        1. in progress
