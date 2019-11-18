# Temp script until https://github.com/deanmalmgren/textract/issues/313 is fixed.

# Between pdftotext 4.00 (the one that ships with git bash 2.18.0) and textract 1.6.1,
# the text files from textract were better (less number of errors).

import sys
import os
import textract


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description='Convert pdf to text'
    )
    parser.add_argument('pdf_file', action='store', help='PDF file to convert')
    parser.add_argument('-o', '--output', action='store', dest='txt_file', default=None)
    res = parser.parse_args()
    return res


if __name__ == '__main__':
    args = parse_arguments()
    pdf_file = args.pdf_file
    txt_file = args.txt_file
    if txt_file is None:
        txt_file = os.path.splitext(pdf_file)[0] + '.txt'
    # print(pdf_file, '->', txt_file)
    text = textract.process(pdf_file)
    with open(txt_file, 'wb') as f:
        f.write(text)
