import time


def degrees2us(degrees:int, PULSE_WIDTH_0:int =500, PULSE_WIDTH_180:int =2500) -> int:
    ''' Convert angle degree to microseconds
        Formula taken from here: https://github.com/fivdi/pigpio/issues/69
    
        Args:
            degree (int): angle degree value
            PULSE_WIDTH_0 (int): pulse width in microseconds for 0 degrees
            PULSE_WIDTH_180 (int): Pulse width in microseconds for 180 degrees
        Return:
            microseconds (float): converted value to microseconds
        '''
    microseconds = PULSE_WIDTH_0 + (degrees / 180) * (PULSE_WIDTH_180 - PULSE_WIDTH_0)
    return int(microseconds)


def test_servo(system, num_tries=3):
    ''' Servo control accuracy is 1us, which is 0.09 degrees'''
    for i in range(num_tries):
        # turn right
        for i in range(50, 140, 1):   
            system.write2register('servo_wheels', degrees2us(i))
            time.sleep(0.005)

        # turn left
        for i in range(140, 50, -1): 
            system.write2register('servo_wheels', degrees2us(i))
            time.sleep(0.005)

    # reset wheels position
    system.write2register('servo_wheels',  degrees2us(90))