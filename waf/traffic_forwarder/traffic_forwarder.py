import tornado.ioloop
import tornado.web
import tornado.httpserver
from detection import isAnomalous,getAttackType
import requests
import urllib.parse
import colorama as cr
import uuid
import datetime
cr.init()
class TrafficHandler(tornado.web.RequestHandler):
    
    # handling get requests
    async def get(self):
        # get request headers
        headers = self.get_headers()
        # get request uri
        uri = self.request.uri
        # get request cookies
        cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
        # unquote the uri
        # parse the uri
        uri=urllib.parse.unquote(uri)
        uri_parsed=urllib.parse.urlparse(uri)
        if uri_parsed.path[-1] == '/':
            data=uri_parsed.path+"index.html"+'?'+uri_parsed.query.replace("+"," ")
        else:
            data = uri_parsed.path+"?"+uri_parsed.query.replace("+"," ")
        if data[-1]=='?':
            data=data[:len(data)-1]
        # print the request
        if data not  in ("/requests","/data","/insert","/status"):
            print(f"{cr.Fore.YELLOW} {data} {cr.Fore.RESET}")
        if data in ("/requests","/data","/insert","/status") or not isAnomalous(str(data)):
            # if the request is safe, forward it to the server
            classType="Normale"
            attackType=""
            if data not  in ("/requests","/data","/insert","/status"):
                print(f"{cr.Fore.GREEN} Normale {cr.Fore.RESET}")
            response = requests.get(uri, headers=headers, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            # if the request is anomalous, return 404
            classType="Anormale"
            attackType=getAttackType(data)
            print(f"{cr.Fore.RED} Anomalous {cr.Fore.RESET}")
            print(f"{cr.Fore.RED} {attackType} {cr.Fore.RESET}")
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)
        # update the requests table
        self.updateRequests("GET",uri_parsed.path,classType,attackType,uri_parsed.query)
    
    # handling post requests
    async def post(self):
        # get request headers
        headers = self.get_headers()
        # get request uri
        uri = self.request.uri
        # get post data
        post_body = self.parse_post_data(self.request.body.decode('utf-8'))
        # creating string for the post data
        post_str=''
        if post_body:
            for key,value in post_body.items():
                post_str+=key + '=' + value + "&"
            post_str=post_str[:len(post_str)-1]
        uri_parsed=urllib.parse.urlparse(uri)
        if uri_parsed.path[-1] == '/':
            data=uri_parsed.path+"index.html"+'?'+post_str.replace("+"," ")
        else:
            data=uri_parsed.path+'?'+post_str.replace("+"," ")
        if data[-1]=='?':
            data=data[:len(data)-1]
        # print the request
        print(f"{cr.Fore.YELLOW} {data} {cr.Fore.RESET}")
        # check if the request is anomalous
        if not isAnomalous(str(data)):
            # if the request is safe, forward it to the server
            classType="Normale"
            attackType=""
            print(f"{cr.Fore.GREEN} Normale {cr.Fore.RESET}")
            cookies = self.parse_cookies(self.request.headers.get('Cookie', 0))
            response = requests.post(uri, headers=headers, data=post_body, cookies=cookies)
            self.set_status(response.status_code)
            self.set_resp_headers(response)
            self.write(response.content)
        else:
            # if the request is anomalous, return 404
            classType="Anormale"
            attackType=getAttackType(data)
            print(f"{cr.Fore.RED} Anormale {cr.Fore.RESET}")
            print(f"{cr.Fore.RED} {attackType} {cr.Fore.RESET}")
            html_404 = open('./template/index.html', 'r').read()
            self.write(html_404)
        # update the database
        self.updateRequests("POST",uri_parsed.path,classType,attackType,post_str)
        
        
    # Helper functions
    def get_headers(self):
        # get request headers
        # return a dictionary of headers
        req_header = {}
        for key, value in self.request.headers.items():
            req_header[key] = value
        return req_header
    
    def set_resp_headers(self, resp):
        # set response headers
        # ignore content-encoding, transfer-encoding and content-length
        # set all other headers
        respheaders = resp.headers
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.set_header(key, respheaders[key])
        self.set_header('Content-Length', len(resp.content))

    def parse_cookies(self, cookie):
        # parse cookies
        # return a dictionary of cookies
        try:
            # create a dictionary of cookies
            cookies = {}
            for line in cookie.split(';'):
                key, value = line.split('=', 1)
                cookies[key] = value
            return cookies
        except:
            pass
    
    def parse_post_data(self, data):
        # parse post data
        # return a dictionary of post data
        try:
            post_data = {}
            for line in data.split('&'):
                key, value = line.split('=', 1)
                value = urllib.parse.unquote(value).replace('+', ' ')
                post_data[key] = value
            return post_data
        except:
            pass

    def updateRequests(self,method,path,classType,attackType,data):
        # preparing request to send to the backend server -> localhost:5000 to store the request
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
        # ignoring the requests sent to the backend server to fetch the data 
        # /insert /data /requests
        if request["Headers"]["Host"] != "localhost:5000":
            url="http://localhost:5000/insert"
            rsp=requests.post(url, json=request)
            return rsp.status_code
        else:
            pass


    
# proxy server configuration
def make_app():
    # return tornado web application object
    return tornado.web.Application([
        (r'.*', TrafficHandler),
    ])

def main():
    # creating a tornado web server
    # listening on port 8080
    # starting the server
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8080)
    print('Started httpserver on port', 8080)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()