import re
import urllib.parse
import requests
import bs4


class ImgLinkInspector(object):
    
    def __init__(self, page_url, **kwargs):
        self.page_url = page_url
        self.src_attr = kwargs.get('src_attr', 'src')
        self.verbose = bool(kwargs.get('verbose', False))

        parsed_url = urllib.parse.urlparse(self.page_url)
        self.default_scheme = parsed_url.scheme
        self.default_scheme_host = f'{parsed_url.scheme}://{parsed_url.netloc}'
        self._re_ignore_images_urls = re.compile(r'^data:', re.I)

    def inspect(self):
        html = self._load_page()
        image_urls = self._find_image_urls(html)
        if self.verbose:
            print(f'{len(image_urls)} image urls found')
        url_statuses = self._check_url_response(image_urls)
        return url_statuses

    def _load_page(self):
        resp = requests.get(self.page_url)
        resp.raise_for_status()
        html = resp.text
        return html

    def _find_image_urls(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        image_elements = soup.findAll('img')
        image_urls = set()
        for el in image_elements:
            src = el['src']
            if not self._re_ignore_images_urls.match(src):
                image_urls.add(self._assert_default_scheme(src))
            else:
                src = el[self.src_attr]
                if not self._re_ignore_images_urls.match(src):
                    image_urls.add(self._assert_default_scheme(src))
        return image_urls

    def _assert_default_scheme(self, url):
        if url.startswith('//'):
            return f'{self.default_scheme}:{url}'
        if url.startswith('/'):
            return f'{self.default_scheme_host}{url}'
        return url

    def _check_url_response(self, image_urls):
        statuses = []
        for url in image_urls:
            url_resp = requests.head(url, allow_redirects=True)
            if url_resp.status_code >= 400 or self.verbose:
                statuses.append((url_resp.status_code, url))

        return statuses
