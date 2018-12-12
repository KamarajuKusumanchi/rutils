import pycodestyle
import os

# To run the tests
# cd into the project directory
# python3 -m pytest


# Todo:- Integrate with latest changes in market_data_processor/tests/test_pep8.py
#   * ignore E501
#   * print statistics at the end
#   * if pycodestyle is not there, use pep8
#   * change variable name result to report

def test_codestyle_conformance():
    '''Test that all code conforms to pep8 standard'''
    codestyle = pycodestyle.StyleGuide(show_source=True)

    # list of python files
    path = '.'
    extension = '.py'
    files = [os.path.join(root, file)
             for root, dirs, files in os.walk(path)
             for file in files
             if file.endswith(extension)]
    print('Checking', files, 'for codestyle conformance.')
    result = codestyle.check_files(files)
    assert result.total_errors == 0, \
        'Found ' + str(result.total_errors) + ' code style errors.'
