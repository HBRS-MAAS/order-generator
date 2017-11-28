import yaml
from random import randint, shuffle, uniform

from delivery import Truck

truck_number = 1


class Bakery(object):
    """docstring for Bakery."""
    def __init__(self, guid, name, location=None,
                 products=[], product_params=None):
        self.guid = "bakery-{:03d}".format(guid)
        self.name = name
        self.location = location
        self.ovens = []
        self.trucks = []
        self.dough_prep_tables = []
        self.kneading_machines = []

        if not products or not product_params:
            print "Error! Missing product list"
        else:
            self.products = []
            shuffle(products)
            for p in range(len(products)):
                x = Product(products[p], product_params)
                self.products.append(x)

    def add_ovens(self, start_id=1, params=None, quantity=2):
        if params:
            quantity = randint(1, params['max'])

        for o in range(start_id, start_id+quantity):
            oven = Oven(o)
            self.ovens.append(oven)

        return start_id + quantity

    def add_trucks(self, start_id=1, params=None, quantity=2, capacity=50):
        if params:
            quantity = randint(1, params['max'])
            capacity = randint(25, params['capacity']*5)/5

        for t in range(start_id, start_id+quantity):
            x = Truck(t, location=self.location, capacity=capacity)
            self.trucks.append(x)

        return start_id + quantity

    def add_kneading_machines(self, start_id=1, params=None, quantity=2):
        if params:
            quantity = randint(1, params['max'])

        for id in range(start_id, start_id+quantity):
            guid = "kneading-machine-{:03d}".format(id)
            self.kneading_machines.append({'guid': guid})

        return start_id + quantity

    def add_prep_tables(self, start_id=1, params=None, quantity=2):
        if params:
            quantity = randint(1, params['max'])

        for id in range(start_id, start_id+quantity):
            guid = "prep-table-{:03d}".format(id)
            self.dough_prep_tables.append({'guid': guid})

        return start_id + quantity

    def update_location(self, location):
        self.location = location
        for truck in self.trucks:
            truck.location = location



class Oven(object):
    """docstring for Oven."""
    def __init__(self, guid, cr=5, hr=5):
        self.guid = "oven-{:03d}".format(guid)
        self.cooling_rate = randint(0, cr)
        self.heating_rate = randint(0, hr)


class Product(object):
    """docstring for Product."""
    def __init__(self, id, params):
        self.guid = id
        self.dough_prep_time = uniform(*params['dough_prep_time'])
        self.resting_time = uniform(*params['resting_time'])
        self.item_prep_time = uniform(*params['item_prep_time'])
        self.breads_per_oven = randint(4, params['breads_per_oven']*2)/2
        self.baking_time = uniform(*params['baking_time'])
        self.baking_temp = uniform(*params['baking_temp'])
        self.cooling_rate = uniform(*params['cooling_rate'])
        self.boxing_temp = uniform(*params['boxing_temp'])
        self.breads_per_box = randint(25, params['breads_per_box']*5)/5
        self.production_cost = uniform(*params['production_cost'])
        self.sales_price = uniform(*params['sales_price'])
