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

    def export(self):
        data = self.__dict__.copy()
        data['trucks'] = [truck.__dict__ for truck in self.trucks]
        data['products'] = [product.__dict__ for product in self.products]
        data['ovens'] = [oven.__dict__ for oven in self.ovens]
        return data


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

        # Preparation
        self.dough_prep_time = randint(*params['dough_prep_time'])
        self.resting_time = randint(*params['resting_time'])
        self.item_prep_time = randint(*params['item_prep_time'])

        # Baking
        self.breads_per_oven = randint(4, params['breads_per_oven'])
        self.breads_per_oven = self.breads_per_oven - self.breads_per_oven % 2
        self.baking_time = randint(*params['baking_time'])
        self.baking_temp = randint(*params['baking_temp'])
        self.baking_temp = self.baking_temp - self.baking_temp % 5
        self.cooling_rate = randint(*params['cooling_rate'])

        # Packaging
        self.boxing_temp = randint(*params['boxing_temp'])
        self.boxing_temp = self.boxing_temp - self.boxing_temp % 5
        self.breads_per_box = randint(5, params['breads_per_box'])
        self.breads_per_box = self.breads_per_box - self.breads_per_box % 5
        self.production_cost = round(uniform(*params['production_cost']), 2)
        self.sales_price = round(uniform(*params['sales_price']), 2)
