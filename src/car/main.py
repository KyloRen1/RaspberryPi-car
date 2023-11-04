import time
import click
from flask import Flask, Response

from src.car.raspi_car import Car


car = Car()
app = Flask(__name__)

@app.route("/turn/<direction>")
def turn(direction):

    if direction == 'left':
        degrees = list(range(90, 140, 1))
    else:
        degrees = list(range(90, 50, -1))

    for i in degrees:   
        car.write2register('servo_wheels', car.degrees2us(i))
        time.sleep(0.005)

    # reset position
    time.sleep(0.5)
    car.write2register('servo_wheels',  car.degrees2us(90))
    
    return Response(status=200)


@app.route("/move/<direction>/<int:speed>")
def movement(direction, speed):
    speed_delta = speed // 100
    speed_values = list(range(0, speed + speed_delta, speed_delta))
    direction = int(direction == 'backward')

    car.speed = speed

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
    for i in speed_values:  
        car.write2register('motor_right', i)
        car.write2register('motor_left', i)
        time.sleep(0.005)
    return Response(status=200)


@app.route("/sound/<int:volume>")
def buzzer(volume):
    car.write2register('buzzer', volume)
    time.sleep(0.5)
    car.write2register('buzzer', 0)
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
    app.run(host=bind_host, port=port, debug=True)


if __name__ == '__main__':
    main()
