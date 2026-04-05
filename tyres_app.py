# main.py
import os

from utils import base_dir
from db import TyreDB
from menus.menu_main import main_menu


def main():
    db_file = os.path.join(base_dir(), "tyres.db")
    db = TyreDB(db_file)
    main_menu(db)


if __name__ == "__main__":
    main()
