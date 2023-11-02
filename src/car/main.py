import click
from http.server import HTTPServer, BaseHTTPRequestHandler



class CarHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.write_reponse(b'')

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)

        self.write_response(body)

    def write_reponse(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8'))


@click.command(help="")
@click.option("--bind-host", default='0.0.0.0', type=str, help="bind host ip")
@click.option("--port", default="5000", type=str, help="port number")
def main(bind_host, port):
    print(f'Listening on http://{bind_host}:{port}')

    server = HTTPServer((bind_host, port), CarHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()