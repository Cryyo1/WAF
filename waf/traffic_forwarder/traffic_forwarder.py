import tornado.ioloop
import tornado.web
import tornado.httpserver
from detection import isAnomalous,getAttackType
import requests
import urllib.parse
from pprint import pprint
import colorama as cr
import uuid
import datetime
cr.init()
class TrafficHandler(tornado.web.RequestHandler):
    async def get(self):
        headers = self.get_headers()
        uri = self.request.uri
        cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
        uri=urllib.parse.unquote(uri)
        uri_parsed=urllib.parse.urlparse(uri)
        data = uri_parsed.path+"?"+uri_parsed.query
        print(f"{cr.Fore.YELLOW} {data} {cr.Fore.RESET}")
        if not isAnomalous(str(data)):
            classType="normale"
            attackType=""
            print(f"{cr.Fore.GREEN} safe {cr.Fore.RESET}")
            response = requests.get(uri, headers=headers, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            classType="anormale"
            attackType=getAttackType(data)
            print(f"{cr.Fore.RED} Anomalous {cr.Fore.RESET}")
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)
        self.updateRequests("GET",uri_parsed.path,classType,attackType,uri_parsed.query)
    async def post(self):
        headers = self.get_headers()
        uri = self.request.uri
        post_body = self.parse_post_data(self.request.body.decode('utf-8'))
        # creating string for the post data
        post_str=''
        for key,value in post_body.items():
            post_str+=key + '=' + value + "&"
        post_str=post_str[:len(post_str)-1]
        uri_parsed=urllib.parse.urlparse(uri)
        data=uri_parsed.path+'?'+post_str
        print(f"{cr.Fore.YELLOW} {data} {cr.Fore.RESET}")
        if not isAnomalous(str(data)):
            classType="normale"
            attackType=""
            print(f"{cr.Fore.GREEN} safe {cr.Fore.RESET}")
            cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
            response = requests.post(uri, headers=headers, data=post_body, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            classType="anormale"
            attackType=getAttackType(data)
            print(f"{cr.Fore.RED} Anomalous {cr.Fore.RESET}")
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)
        self.updateRequests("POST",uri_parsed.path,classType,attackType,post_str)
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

    def updateRequests(self,method,path,classType,attackType,data):
        request={
            "Method":method,
            "Path":path,
            "Class":classType,
            "Type":attackType,
            "Headers":self.get_headers(),
            "Data":data,
            "Id":str(uuid.uuid1()).split('-')[0],
            "Date time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        url="http://localhost:5000/insert"
        rsp=requests.post(url, json=request)
        return rsp.status_code
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
