from glob import glob
import os


def pick_first_file(dir, file_glob):
    dir = os.path.abspath(os.path.expanduser(dir))
    file_list = glob(os.path.join(dir, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list)[0]


def pick_last_file(dir, file_glob):
    dir = os.path.abspath(os.path.expanduser(dir))
    file_list = glob(os.path.join(dir, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list, reverse=True)[0]
