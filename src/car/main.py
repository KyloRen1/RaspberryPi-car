import click
from http.server import HTTPServer, BaseHTTPRequestHandler
import ujson as json
import cgi
import urllib


from src.car.raspi_car import Car


system = Car()

'''
class CarHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(body)
            key = data.get('key')
            status = data.get('status')

            if key == 's' and status in ['pressed', 'released']:
                volume = 500 if status == 'pressed' else 0
                system.write2register('buzzer', volume)
                self.send_response(200)
            else:
                self.send_response(400)
        except json.JSONDecodeError:
            self.send_response(400)
    
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Request processed'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

'''

from flask import Flask, render_template, request, Response
app = Flask(__name__)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 's':
        block = 'buzzer'
    
    if action == 'pressed':
        system.write2register('buzzer', 500)
    elif action == 'released':
        system.write2register('buzzer', 0)
    
    return Response(status=200)

        

@click.command(help="")
@click.option("--bind-host", default='0.0.0.0', type=str, help="bind host ip")
@click.option("--port", default=5000, type=int, help="port number")
def main(bind_host, port):
    #print(f'Listening on http://{bind_host}:{port}')

    #server = HTTPServer((bind_host, port), CarHTTPRequestHandler)
    #server.serve_forever()

    ######################

    app.run(host=bind_host, port=port, debug=True)


if __name__ == '__main__':
    main()
