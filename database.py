# -*- coding: utf-8 -*-

import psycopg2

class Database:
    def __init__(self):
        self._conn = psycopg2.connect(database='ninedict', host='gardenia.csie.ntu.edu.tw', user='ninegag', password='agent#336')
        self._cursor = self._conn.cursor()

    def _add_slashes(self, string):
        string = string.encode('utf8')
        string = re.sub(r"\\", r"\\\\", string)
        string = re.sub("'", r"\\'", string)
        return string

