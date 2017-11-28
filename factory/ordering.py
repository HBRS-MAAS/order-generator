#!/usr/bin/env python

from random import randint, random
import yaml


class Order(object):
    """docstring for Order."""
    def __init__(self, guid, customer, category=1, order_day=0, delta=1,
                 products={}):
        file_stream = open('config/products.yaml', 'r')
        product_types = yaml.load(file_stream)

        self.guid = "order-{:03d}".format(guid)
        self.customer_id = customer
        self.order_date = {"day": order_day, "hour": randint(0, 12)}
        self.delivery_date = {"day": order_day+delta, "hour": randint(0, 23)}
        if not products:
            self.products = {}
            # TODO remove this hardcoded choice
            for p in product_types[:5]:
                self.products[p] = randint(0, 10)
        else:
            self.products = products


class Customer(object):
    """docstring for Customer."""
    def __init__(self, guid, name, category=1, location=None):
        self.guid = "customer-{:03d}".format(guid)
        self.name = name
        self.location = location
        self.type = category

    def order(self, days, order_num):
        """
        days: days in the scenario
        order_num: On which order number to start
        """
        orders = []
        for day in range(1, days+1):
            delta = None
            if self.type == 1 or self.type == 2:
                delta = 1
            elif self.type == 3 and random() > 0.2:
                delta = randint(2, days+1)

            if delta:
                order = Order(order_num, self.guid, order_day=day, delta=delta)
                orders.append(order)
                order_num = order_num + 1

            if self.type == 1 and random() > 0.5:
                order = Order(order_num, self.guid, order_day=day+1, delta=0)
                orders.append(order)
                order_num = order_num + 1

        return orders, order_num
