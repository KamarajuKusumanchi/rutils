#! /usr/bin/env python3

# Situation:
# The pdfannots program ([1], [2]) extracts annotations (highlights,
# comments, etc.) from a PDF file and formats them as markdown.
#
# [1] - https://pypi.org/project/pdfannots/ - location of pdfannots on PyPi
# [2] - https://github.com/0xabu/pdfannots - source code of pdfannots
#
# The output might be something like:
#------------------------------------------------------------------------------
# ## Highlights
#
#  * Page #2:
#    > Lending against a portfolio is safer, for the lender
#  * Page #3:
#    > "arbitrage on collateralized bundles of obscure financial contracts,"
#
#  * Page #5: "the flotation price"
#------------------------------------------------------------------------------
# The idea here is to remove the page numbers lines and transform it into
# something like:
#------------------------------------------------------------------------------
#
#  Lending against a portfolio is safer, for the lender
#
#  "arbitrage on collateralized bundles of obscure financial contracts,"
#
#  "the flotation price"
#------------------------------------------------------------------------------
#
# Why is this important to me?
# Sometimes, I export long html pages (ex:- Matt Levine's articles) to pdf
# and read it in a pdf reader, so I can highlight and store the annotated text.
# In this type of scenario, the page numbers are a bit meaning less. So I want
# to remvoe them.
import re
import sys
import textwrap


def remove_page_numbers(input_file, output_file=sys.stdout):
    for line in input_file:
        line = process_line(line)
        if line is not None:
            lines = format_line(line)
            print(lines, file=output_file)

def process_line(line):
    # Return the processed line.
    # If a line is to be removed, return None instead of string.

    line = line.strip()
    if line == '## Highlights':
        return None

    # Removed lines such as
    # * Page #1:
    # * Page #10:
    if re.fullmatch('\* Page #[\d]+:', line):
        return None

    if line.startswith('> '):
        return line[2:]

    # Convert lines such as
    # * Page #5: "the flotation price"
    # to
    # "the flotation price"
    m = re.search('\* Page #[\d]+: (.+)$', line)
    if m:
        return m.group(1)

    return line

def format_line(line):
    # To make the output look same as what we get from vim's gq command.
    width=79
    lines = textwrap.fill(line, width)
    return lines

if __name__ == '__main__':
    remove_page_numbers(sys.stdin)

# See also:
# * https://github.com/amano41/pdf-annotations/blob/main/md2sb.py
#   - used the code from here and adopted it to my use case.