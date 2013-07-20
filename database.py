# -*- coding: utf-8 -*-

import psycopg2

class Database:
    def __init__(self):
        self._conn = psycopg2.connect(database='ninecrawl', host='gardenia.csie.ntu.edu.tw', user='ninegag', password='agent#336')
        self._cursor = self._conn.cursor()

    def _add_slashes(self, string):
        string = string.encode('utf8')
        string = re.sub(r"\\", r"\\\\", string)
        string = re.sub("'", r"\\'", string)
        return string

    def get_latest_gags(self, num_gags=10):
        cmd = '''SELECT gag_id, title, content_url
                 FROM gag
                 WHERE crawl_time IS NOT NULL
                       AND title IS NOT NULL
                       AND (
                          type = 'IM'
                          OR type = 'GI'
                       )
                 ORDER BY crawl_time DESC 
                 LIMIT %s''' % num_gags
        self._cursor.execute(cmd)
        res = self._cursor.fetchall()
        return res

