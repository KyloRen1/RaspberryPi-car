import pytest

from src.car.raspi_car import Car

@pytest.fixture(scope="module")
def system():
    module = Car()
    return module