#!/usr/bin/python3

import os
from glob import glob
from pathlib import Path
import shutil


BOOKMARK_DIR = "/media/ncs/Ventoy/extracted/bookmarks"
CHROME_PROFILE_PATH = "/home/ncs/.config/google-chrome/"


def create_dir(path) -> bool:
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


def copy_bookmark():
    create_dir(BOOKMARK_DIR)
    files = glob(f"{CHROME_PROFILE_PATH}*/Bookmarks")

    for file in files:
        profile = os.path.basename(str(Path(os.path.join(file, "..")).resolve())).replace(" ", "_")
        profile_path = os.path.join(BOOKMARK_DIR, profile)
        create_dir(profile_path)
        shutil.copy(file, os.path.join(BOOKMARK_DIR, profile))


def main() -> None:
    copy_bookmark()


if __name__ == "__main__":
    main()
