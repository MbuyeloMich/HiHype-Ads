#!/usr/bin/env python3
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.dirname(os.path.abspath(__file__))


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        url_path = urlsplit(path).path
        if url_path in ('', '/'):
            return os.path.join(ROOT, 'index.html')

        cleaned = url_path.lstrip('/')
        if not cleaned:
            return os.path.join(ROOT, 'index.html')

        if os.path.exists(os.path.join(ROOT, cleaned)):
            return os.path.join(ROOT, cleaned)

        if not os.path.splitext(cleaned)[1]:
            html_path = os.path.join(ROOT, cleaned + '.html')
            if os.path.exists(html_path):
                return html_path

        if cleaned.endswith('/'):
            directory_path = os.path.join(ROOT, cleaned.rstrip('/'))
            if os.path.isdir(directory_path):
                index_path = os.path.join(directory_path, 'index.html')
                if os.path.exists(index_path):
                    return index_path

        return os.path.join(ROOT, '404.html')

    def do_GET(self):
        split_url = urlsplit(self.path)
        url_path = split_url.path

        if url_path in ('', '/'):
            self.path = '/index.html'
            return super().do_GET()

        cleaned = url_path.lstrip('/')
        if cleaned and not os.path.splitext(cleaned)[1]:
            page_path = os.path.join(ROOT, cleaned + '.html')
            if os.path.exists(page_path):
                self.path = '/' + cleaned + '.html'
                return super().do_GET()

        if url_path.endswith('/'):
            directory_path = os.path.join(ROOT, url_path.strip('/'))
            if os.path.isdir(directory_path):
                index_path = os.path.join(directory_path, 'index.html')
                if os.path.exists(index_path):
                    self.path = url_path + 'index.html'
                    return super().do_GET()

        return super().do_GET()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    server = ThreadingHTTPServer((host, port), SiteHandler)
    print(f'Serving Hi Hype Ads site at http://{host}:{port}')
    server.serve_forever()
