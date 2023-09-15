import os
import constants as cn
import sqlite3

class ConnectorFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_connector():
        db_path = os.path.join(cn.db_folder,cn.db_file)
        return sqlite3.connect(db_path)