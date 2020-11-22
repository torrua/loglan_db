# -*- coding: utf-8 -*-
"""Main app page"""

from loglan_db import app_lod
from loglan_db.model import Word

if __name__ == "__main__":

    with app_lod().app_context():
        pass
