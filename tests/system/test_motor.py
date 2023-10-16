import time
import pytest

@pytest.mark.parametrize("max_speed, n_points", [(1000, 100), (10000, 100)])
def test_motor(max_speed, n_points, system):
    speed_delta = max_speed // n_points
    speed = list(range(0, max_speed + speed_delta, speed_delta))
    speed_values = speed + speed[::-1]

    # forward movement
    system.write2register('motor_direction_right', 0)
    system.write2register('motor_direction_left', 0)
    for i in speed_values:  
        system.write2register('motor_right', i)
        system.write2register('motor_left', i)
        time.sleep(0.005)
    
    time.sleep(1)

    # backward movement
    system.write2register('motor_direction_right', 1)
    system.write2register('motor_direction_left', 1)
    for i in speed_values:  
        system.write2register('motor_right', i)
        system.write2register('motor_left', i)
        time.sleep(0.005)