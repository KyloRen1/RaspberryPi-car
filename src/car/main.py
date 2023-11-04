import click
from http.server import HTTPServer, BaseHTTPRequestHandler
import ujson as json
import cgi
import urllib
import time

from src.car.raspi_car import Car


car = Car()

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


@app.route("/move/<direction>/<int:speed>")
def movement(direction, speed):
    speed_delta = speed // 100
    speed_values = list(range(0, speed + speed_delta, speed_delta))
    direction = int(direction == 'forwards')

    print(speed_values)
    car.speed = speed
    car.direction = direction

    car.write2register('motor_direction_right', direction)
    car.write2register('motor_direction_left', direction)
    for i in speed_values:  
        car.write2register('motor_right', i)
        car.write2register('motor_left', i)
        time.sleep(0.005)

    return Response(status=200)


@app.route('/stop')
def stop():
    speed_delta = car.speed // 100
    speed_values = list(range(0, car.speed + speed_delta, speed_delta))[::-1]

    car.speed = 0

    car.write2register('motor_direction_right', car.direction)
    car.write2register('motor_direction_left', car.direction)

    for i in speed_values:  
        car.write2register('motor_right', i)
        car.write2register('motor_left', i)
        time.sleep(0.005)
    return Response(status=200)






@app.route("/sound/<int:volume>")
def buzzer(volume):
    car.write2register('buzzer', volume)
    return Response(status=200)


@app.route("/led/<int:r>/<int:g>/<int:b>")
def lights(r, g, b):
    car.write2register('rgbled_io1', r)
    car.write2register('rgbled_io2', g)
    car.write2register('rgbled_io3', b)
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
