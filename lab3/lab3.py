from http.server import BaseHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from http.server import HTTPServer


class ServerWorking(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("<html><head><meta charset='utf-8'><title>Лаба 3 Питон</title></head>", "utf-8"))
        self.wfile.write(bytes("<h1>Лаба 3 Питон</h1>", "utf-8"))
        self.wfile.write(bytes("<p>%s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


# serv_address = ('', 8080)
# serv = HTTPServer(serv_address, ServerWorking)
# serv.serve_forever()

cgi_address = ('localhost', 8080)
cgi = HTTPServer(cgi_address, CGIHTTPRequestHandler)
cgi.serve_forever()
