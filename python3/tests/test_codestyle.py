from pycodestyle import StyleGuide
import os

# To run the tests
# cd into the project directory
# python3 -m pytest


def test_codestyle_conformance():
    """Test that all code conforms to pep8 standard"""
    test_path = os.path.dirname(__file__)
    codestyle = StyleGuide(show_source=True,
                           config_file=os.path.join(test_path, '../setup.cfg'))

    # list of python files
    path = '.'
    extension = '.py'
    files = [os.path.join(root, file)
             for root, dirs, files in os.walk(path)
             for file in files
             if file.endswith(extension)]
    print('Checking', files, 'for codestyle conformance.')
    report = codestyle.check_files(files)
    report.print_statistics()
    assert report.total_errors == 0, \
        'Found ' + str(report.total_errors) + ' code style errors.'
