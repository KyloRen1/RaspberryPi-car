import time
import pytest

@pytest.mark.parametrize("volume", [100, 500, 1000])
def test_buzzer(volume, system):
    # sound on 
    system.write2register('buzzer', volume)
    time.sleep(1)
    # sound off
    system.write2register('buzzer', 0)