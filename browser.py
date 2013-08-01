import mechanize
import cookielib
import time

class Browser:
    def __init__(self):
        self._br = mechanize.Browser()
        self._set_cookie_jar()
        self._set_options()

    def _set_cookie_jar(self):
        cj = cookielib.LWPCookieJar()
        self._br.set_cookiejar(cj)

    def _set_options(self):
        self._br.set_handle_equiv(True)
        self._br.set_handle_redirect(True)
        self._br.set_handle_referer(True)
        self._br.set_handle_robots(False)
        self._br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def _get_page_content(self, url):
        okay = False
        while not okay:
            try:
                page = self._br.open(url)
                okay = True
            except:
                print url
                print 'mechanize error... sleep for 10 seconds'
                time.sleep(10)
        content = page.read()
        return content

