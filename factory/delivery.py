from random import randint, uniform
import networkx as nx
import json
from utils import location
import os
import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


class Truck(object):
    """docstring for Truck."""
    def __init__(self, guid, location, capacity=50):
        self.guid = "truck-{:03d}".format(guid)
        self.load_capacity = randint(10, capacity*5)/5
        self.location = location


class StreetNetwork(object):
    def __init__(self, customers, bakeries, size):
        G = nx.Graph()
        pos = {}
        self.mapping = {}
        self.bakery_nodes = []
        self.customer_nodes = []

        n = customers + bakeries
        F = nx.connected_watts_strogatz_graph(n, 3, 0.5)
        remap = {n: n+1 for n in F.nodes()}
        self.F = nx.relabel_nodes(F, remap, copy=False)

        self.pos = nx.spring_layout(F, iterations=500, scale=10.0)

        self.node_id = 1

        self.G = G

    def add_node(self, company, category):
        guid = "node-{:03d}".format(self.node_id)
        loc = location(self.pos[self.node_id])
        self.G.add_node(self.node_id, company=company.guid, name=company.name,
                        guid=guid, type=category, location=loc)
        self.mapping[self.node_id] = guid
        self.node_id = self.node_id + 1

        if category is 'bakery':
            self.bakery_nodes.append(self.node_id)
        elif category is 'customer':
            self.customer_nodes.append(self.node_id)

        return loc

    def add_streets(self):
        self.G.add_edges_from(self.F.edges())
        self.G = nx.relabel_nodes(self.G, self.mapping, copy=False)
        self.G = self.G.to_directed()

        edge_id = 1
        for edge in self.G.edges():
            self.G.edges[edge]['guid'] = "edge-{:03d}".format(edge_id)
            edge_id = edge_id + 1

            # Add euclidean distance multiplied by some value
            loc1 = self.G.nodes[edge[0]]['location']
            loc2 = self.G.nodes[edge[1]]['location']
            dist = ((loc1['x']-loc2['x'])**2 + (loc2['y']-loc2['y'])**2)**0.5
            self.G.edges[edge]['dist'] = dist * uniform(1.0, 2.0)

    def draw(self, filename=None, verbose=False):
        nx.draw(self.F, self.pos, font_size=11, node_size=500,
                with_labels=True,
                node_color='w')
        nx.draw_networkx_nodes(self.F, self.pos, nodelist=self.bakery_nodes,
                               node_color='c',
                               node_shape='s', node_size=800)
        if filename:
            plt.savefig("scenarios/%s-scenario.png" % filename)
        if verbose:
            plt.show()

    def export(self):
        data = nx.node_link_data(self.G)
        # dest = 'street_network.json'
        del data['graph']
        del data['multigraph']

        for node in data['nodes']:
            del node['id']

        # with open(dest, 'w') as f:
        #     json.dump(data, f, indent=2)

        return data

    def get_graph(self):
        return self.G
