"""
    An application can extract content in pdf file into mysql server and store them
"""
from pathlib import Path
import pdfplumber
import json
import os
import glob
import re
from tqdm import tqdm
import nltk.corpus
from nltk.corpus import stopwords
nltk.download('stopwords')


class Directory:
    """Represents a directory path for input or output of PDF files."""
    def init(self) -> None:
        """Prompts the user to input a directory path and stores it as a Path object."""
        dir = input("Please enter the directory path (not including the pdf): ")
        self.dir = Path(dir)


class DirInput(Directory):
     """Prompts the user to specify whether to scan an individual PDF or an entire directory, and
        prompts for the appropriate input, and stores the list of PDF files as an attribute."""
     def init(self) -> None:
        dir_type = input("Do you want to scan one individual pdf or an entire directory? (Type 'pdf' or 'dir') ")
        if dir_type == 'pdf':
            dir = input("Please enter the full pdf path for data input: ")
            self.pdf_files = [dir]
        elif dir_type == 'dir':
            dir = input("Please enter the directory path: ")
            self.pdf_files = tqdm(glob.glob(os.path.join(dir, '*.pdf')))
            if not self.pdf_files:
                raise Exception("No PDF files in the directory.")
        else:
            raise Exception("Invalid input. Please enter 'pdf' or 'dir'.")
        self.dir = Path(dir)


class DirOutput(Directory):
    def init(self) -> None:
        dir = input("Please enter the full directory path for output: ")
        self.dir = Path(dir)


def extract_content(pdf_path):
    """Extracts the text content of a PDF file and returns a list of dictionaries, where each dictionary
    contains a paragraph number and its corresponding text.

    Args:
        pdf_path (str): The file path to the PDF file to extract content from.

    Returns:
        content (list): A list of dictionaries, where each dictionary represents a paragraph and contains a 
        paragraph number and its corresponding text.
    """
    #extracting text with pdfplumber, initialize full text variable to extract to.
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=False,
                use_text_flow=False,
                horizontal_ltr=True,
                vertical_ttb=True,
                extra_attrs=[],
                split_at_punctuation=False
            )
        #Split string with newline seperator
        paragraphs = full_text.split("\n")
        #Initialize paragraph count and variables
        current_paragraph = ""
        paragraph_number = 1
        content = []
        for paragraph in paragraphs:
            paragraph = clean_paragraph(paragraph)
            #Strip whitespace
            if paragraph.strip() == "":
                #Check if paragraph is empty. If it is, clear string and add paragraph count, append text
                if current_paragraph != "":
                    content.append({"paragraph_number": paragraph_number, "text": current_paragraph})
                    current_paragraph = ""
                    paragraph_number += 1
            else:
                #Append current paragraph to paragraph
                current_paragraph += " " + paragraph
        if current_paragraph != "":
            #Once all paragraphs are processed, append to the content list
            content.append({"paragraph_number": paragraph_number, "text": current_paragraph})
    return content

def clean_paragraph(paragraph):
    # step 1: Normalize Text
    paragraph = paragraph.lower()

    # Step 2: Remove Unicode Characters
    paragraph = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)|^rt|http.+?", "", paragraph)

    # Step 3: Remove Stopwords
    stop = stopwords.words('english')
    paragraph = " ".join([word for word in paragraph.split() if word not in (stop)])

    return paragraph


def main():
    """The main function of the script that extracts the content from each PDF file in the input directory,
    saves the content as a list of dictionaries, and outputs the content as a JSON file in the output directory."""
    dirinput = DirInput()
    diroutput = DirOutput()
    dirinput.init()
    diroutput.init()
    content = []
    for pdf_file in dirinput.pdf_files:
        content = extract_content(pdf_file)
        #split filename from the extension, add .json to the end
        output_file = os.path.splitext(os.path.basename(pdf_file))[0] + ".json"
        #construct full path
        output_path = os.path.join(diroutput.dir, output_file)
        #Error handling to check if files exist
        while os.path.exists(output_path):
            exist_choice = input(f"The file {output_file} already exists within the directory. Type 'O' to overwrite, or 'N' to change the file name.")
            if exist_choice == "O" or exist_choice == "o":
                break
            elif exist_choice == "N" or exist_choice == "n":
                new_file = input(" Enter the new file name:")
                output_file = new_file + ".json"
                output_path = os.path.join(diroutput.dir, output_file)
                print(f"File name changed to {output_file}.")
            else:
                print("Invalid option, try again.")
        jsonString = json.dumps(content)
        with open(output_path, "w") as jsonFile:
            jsonFile.write(jsonString)
            jsonFile.close()

if __name__ == "__main__":
    main()

