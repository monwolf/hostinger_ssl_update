import mechanize
import cookielib
import urlparse
import sys

if sys.version_info >= (2, 7):
    from bs4 import BeautifulSoup
    bs4 = True
else:
    from BeautifulSoup import BeautifulSoup
    bs4 = False


class Hostinger(object):
    _class_test_login = "user"
    _tag_test_login = "li"
    _debug = True
    _cpanel_ssl_path = "/advanced/ssl/aid/"

    def __init__(self, config):
        self.config = config
        self.br = None
        self.base_url = None

    def _create_browser(self):
        # Browser
        self.br = mechanize.Browser()
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)

        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        self.br.set_debug_http(self._debug)
        self.br.set_debug_redirects(self._debug)
        self.br.set_debug_responses(self._debug)

        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0')]

    def _login(self):
        if not self.br:
            self._create_browser()
        self.br.open(self.config["hostinger"]['cpanel_url'])
        self.br.select_form(nr=0)
        self.br.form['email'] = self.config["hostinger"]['username']
        self.br.form['password'] = self.config["hostinger"]['password']
        self.br.submit()
        r = self.br.response()

        if bs4:
            soup = BeautifulSoup(r.read(), 'html5lib')
        else:
            soup = BeautifulSoup(r.read())
        try:
            if bs4:
                soup.find_all(self._tag_test_login, {'class': self._class_test_login})[0]
            else:
                soup.findAll({self._tag_test_login: True, 'class': self._class_test_login})[0]
        except Exception:
            raise Exception("Login Failed")
        url = urlparse.urlparse(r.geturl())
        self.base_url = url.scheme + "://" + url.netloc

    @staticmethod
    def __read_file(filename):
        with open(filename, 'r') as content_file:
            content = content_file.read()
        return content

    def load_ssl(self):
        if not self.base_url:
            self._login()
        url = self.base_url + self._cpanel_ssl_path + self.config["hostinger"]['hosting_id']
        self.br.open(url)
        # print(self.br.response().read())
        self.br.select_form(id='advanced-php-config-form')
        print(self.br.form)
        items = self.br.form.find_control("domain").items
        assigned = False
        for item in items:
            if self.config['ssl']['domain'] == item.name:
                self.br.form["domain"] = [item.name]
                assigned = True
                break
        print(self.br.form["domain"])
        if not assigned:
            raise Exception("Domain " + self.config['ssl']['domain'] + "not found")
        self.br.form["crt"] = self.__read_file(self.config['ssl']['crt'])
        self.br.form["key"] = self.__read_file(self.config['ssl']['key'])
        if self.config['ssl']['ca_crt']:
            self.br.form["bundle"] = self.__read_file(self.config['ssl']['ca_crt'])
        self.br.submit()
