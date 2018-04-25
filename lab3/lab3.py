from http.server import CGIHTTPRequestHandler
from http.server import HTTPServer

cgi_address = ('localhost', 8080)
cgi = HTTPServer(cgi_address, CGIHTTPRequestHandler)
cgi.serve_forever()
