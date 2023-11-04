import time
import pytest

@pytest.mark.parametrize("r, g, b", [
    (1, 1, 0), # blue
    (1, 0, 1), # green
    (0, 1, 1), # red
    (0, 1, 0), # pink
    (0, 0, 1), # yellow / green
    (1, 0, 0), # cyan
    (0, 0, 0), # reset
])
def test_rgbled(r, g, b, system):
    # color update
    system.write2register('rgbled_io1', r)
    system.write2register('rgbled_io2', g)
    system.write2register('rgbled_io3', b)
    time.sleep(1)
    # color reset
    system.write2register('rgbled_io1', 1)
    system.write2register('rgbled_io2', 1)
    system.write2register('rgbled_io3', 1)