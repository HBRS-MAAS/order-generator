from random import randint
from utils import location


class Truck(object):
    """docstring for Truck."""
    def __init__(self, guid, location, capacity=50):
        self.guid = "truck-{:03d}".format(guid)
        self.load_capacity = randint(10, capacity*5)/5
        self.location = location


