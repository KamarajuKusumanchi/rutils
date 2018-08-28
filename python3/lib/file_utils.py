from glob import glob
from datetime import datetime
import os
import shutil


def pick_first_file(dir_name, file_glob):
    dir_name = os.path.abspath(os.path.expanduser(dir_name))
    file_list = glob(os.path.join(dir_name, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list)[0]


def pick_last_file(dir_name, file_glob):
    dir_name = os.path.abspath(os.path.expanduser(dir_name))
    file_list = glob(os.path.join(dir_name, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list, reverse=True)[0]


def rename_with_timestamp(src):
    # Given a file or directory src, move it to src_asof_YYYYMMDD_HHmmSS where
    # YYYYMMDD_HHmmSS is the last modified time. This function is useful to
    # take a backup before something else overwrites the original source.
    #
    # If the destination file/directory already exists, do not overwrite it.
    #
    # Get the absolute path since src can contain something like '.' and '..'
    src = os.path.abspath(os.path.expanduser(src))
    if not os.path.exists(src):
        return
    mtime = os.path.getmtime(src)
    timestamp = datetime.fromtimestamp(mtime).strftime('%Y%m%d_%H%M%S')
    dst = src + '_asof_' + timestamp
    if not os.path.exists(dst):
        shutil.move(src, dst)
        print(src, ' -> ', dst)
    else:
        print(src, ' --> ', dst)


def backup_with_timestamp(src, target_dir=None):
    # Given a file or directory src, copy it to src_asof_YYYYMMDD_HHmmSS where
    # YYYYMMDD_HHmmSS is the last modified time. This function is useful to
    # take a backup before something else overwrites the original source.
    #
    # If the destination file/directory already exists, do not overwrite it.
    #
    # If target_dir is specified, src is copied into it.
    #
    # Get the absolute path since src can contain something like '.' and '..'
    src = os.path.abspath(os.path.expanduser(src))
    if not os.path.exists(src):
        return
    mtime = os.path.getmtime(src)
    timestamp = datetime.fromtimestamp(mtime).strftime('%Y%m%d_%H%M%S')

    if target_dir is None:
        target_dir = os.path.dirname(src)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    base_name = os.path.basename(src)
    dst = os.path.join(target_dir, base_name + '_asof_' + timestamp)

    if not os.path.exists(dst):
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)
        print(src, ' -> ', dst)
    else:
        print(src, ' --> ', dst)
