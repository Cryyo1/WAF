import tornado.ioloop
import tornado.web
import tornado.httpserver
from detection import filter
import requests
import urllib.parse
from pprint import pprint

class TrafficHandler(tornado.web.RequestHandler):
    async def get(self):
        headers = self.get_headers()
        url = self.request.uri
        cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
        query = urllib.parse.urlparse(urllib.parse.unquote(url)).query.replace('+', ' ')
        if query.replace(' ', '') == '':
            query = "empty"
        if not filter(str(query)):
            print(url)
            response = requests.get(url, headers=headers, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)
    
    async def post(self):
        headers = self.get_headers()
        url = self.request.uri
        post_body = self.parse_post_data(self.request.body.decode('utf-8'))
        if not filter(str(post_body)):
            cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
            response = requests.post(url, headers=headers, data=post_body, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)

    # Helper functions
    def get_headers(self):
        req_header = {}
        for key, value in self.request.headers.items():
            req_header[key] = value
        return req_header
    
    def set_resp_headers(self, resp):
        respheaders = resp.headers
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.set_header(key, respheaders[key])
        self.set_header('Content-Length', len(resp.content))

    def parse_cookies(self, cookie):
        cookies = {}
        for line in cookie.split(';'):
            key, value = line.split('=', 1)
            cookies[key] = value
        return cookies
    
    def parse_post_data(self, data):
        post_data = {}
        for line in data.split('&'):
            key, value = line.split('=', 1)
            value = urllib.parse.unquote(value).replace('+', ' ')
            post_data[key] = value
        return post_data

def make_app():
    return tornado.web.Application([
        (r'.*', TrafficHandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8080)
    print('Started httpserver on port', 8080)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
