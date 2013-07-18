import json
import urllib
import config
from browser import Browser

class BaseKeyworder:
    def __init__(self):
        self._br = Browser()

    def _get_word_id(self, gag_id, word_str):
        args = {
            'gag_id': gag_id,
            'user_id': config.admin_id,
            'valid_key': config.admin_key,
            'word_str': word_str,
        }
        url = 'http://disa.csie.org:5566/lookup/recomm/id/?' + urllib.urlencode(args)
        content = self._br._get_page_content(url)
        result = json.loads(content)
        assert result['status'] == 'OKAY'
        return result['respond']['id']

    def _add_recomm(self, gag_id, word_id):
        args = {
            'gag_id': gag_id,
            'user_id': config.admin_id,
            'valid_key': config.admin_key,
            'word_id': word_id,
        }
        url = 'http://disa.csie.org:5566/lookup/explain/query/?' + urllib.urlencode(args)
        content = self._br._get_page_content(url)
        result = json.loads(content)
        return result['status'] == 'OKAY'

    def _add_keyword(self, gag_id, keyword):
        word_id = self._get_word_id(gag_id, keyword)
        assert word_id
        success = self._add_recomm(gag_id, word_id)
        assert success

class MemeKeyworder(BaseKeyworder):
    def add_keyword(self, gag_id, image_url):
        self._add_keyword(gag_id, 'deserve')

