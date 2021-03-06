# from doser import Doser
from doser import Doser
from http.server import(BaseHTTPRequestHandler, HTTPServer)
import json

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        config = json.loads(open('./secrets.json').read())
        stop_words = [line.rstrip('\n') for line in open('./french_stop_words.txt')]
        swear_words = [line.rstrip('\n') for line in open('./french_swear_words.txt')]

        doser = Doser(config['file'], config['people'], stop_words, swear_words)
        message = json.dumps(doser.parse())

        self.wfile.write(bytes(message, 'utf8'))

        return

def run():
    print('Starting server...')

    server_address = ('127.0.0.1', 3003)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('Running server...')
    httpd.serve_forever()

run()
