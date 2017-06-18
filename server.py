# from doser import Doser
from doser import Doser
from http.server import(BaseHTTPRequestHandler, HTTPServer)
import json

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        config_file = open('./secrets.json').read()
        config = json.loads(config_file)

        stopwords = [line.rstrip('\n') for line in open('./french_stopwords.txt')]
        swearwords = [line.rstrip('\n') for line in open('./french_swearwords.txt')]

        doser = Doser(config['file'], config['people'], stopwords, swearwords)
        doser.parse()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        message = json.dumps(doser.export())
        self.wfile.write(bytes(message, 'utf8'))

        return

def run():
    print('Starting server...')

    server_address = ('127.0.0.1', 3003)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('Running server...')
    httpd.serve_forever()

run()
