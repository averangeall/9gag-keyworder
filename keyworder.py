import os
import re
import json
import urllib
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
import config
from browser import Browser
from memeclass import MemeClassifier
import engvoc

class BaseKeyworder(object):
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
    def __init__(self):
        super(MemeKeyworder, self).__init__()
        self._classifier = MemeClassifier('templates')

    def add_keyword(self, gag_id, image_url):
        ret = os.system("bash download.sh '%s' '%s'" % (gag_id, image_url))
        assert ret == 0
        which = self._classifier.classify('images/%s.jpg' % gag_id)
        if which:
            print 'meme', which
            self._add_keyword(gag_id, which)

class VocKeyworder(BaseKeyworder):
    def __init__(self):
        super(VocKeyworder, self).__init__()
        self._vocs = engvoc.voc2000
        self._lemmatizer = WordNetLemmatizer()
        self._stemmer1 = LancasterStemmer()
        self._stemmer2 = SnowballStemmer('english')

    def add_keyword(self, gag_id, title):
        tokens = re.split(' |\.|,|;|=', title)
        for token in tokens:
            token = re.sub(r"\W+$", '', token)
            token = re.sub(r"^\W+", '', token)
            vocs = []
            try:
                token = token.encode('utf8')
                vocs.append(re.sub(r"'\w+", '', token).lower())
                vocs.append(self._lemmatizer.lemmatize(vocs[0]))
                vocs.append(self._stemmer1.stem(vocs[0]))
                vocs.append(self._stemmer2.stem(vocs[0]))
            except UnicodeDecodeError:
                continue
            if vocs[0] == '':
                continue
            try:
                float(vocs[0])
                continue
            except ValueError:
                pass
            if not any([voc in self._vocs for voc in vocs]):
                print 'voc', vocs, token
                self._add_keyword(gag_id, token)

