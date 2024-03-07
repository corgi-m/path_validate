import os
import random
from Crypto.PublicKey import RSA

from model.RSAManager import RSAManager


class Network:
    def __init__(self, ):
        self.__nodes = {}
        self.__edges = {}

    def set_network(self, G):
        for node_index in G.nodes:
            self.__nodes[node_index] = Node(node_index)

        edge_index = 0
        for edge in G.edges:
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[0]], self.__nodes[edge[1]])
            self.__nodes[edge[0]].add_route(edge[1], self.__edges[edge_index])
            edge_index += 1
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[1]], self.__nodes[edge[0]])
            self.__nodes[edge[1]].add_route(edge[0], self.__edges[edge_index])
            edge_index += 1

    def get_nodes(self):
        return self.__nodes

    def get_edges(self):
        return self.__edges


class Node:
    def __init__(self, name):
        self.__name = str(name)
        self.__routing_table = {}  # 路由表
        self.packages = []
        (self.SK, self.PK) = RSAManager.load_keys(os.getenv('RandomSeed'), self.__name)

    def __repr__(self):
        return "Node: " + self.__name + ": " + str(list(self.__routing_table.values()))

    def get_name(self):
        return self.__name

    def get_routing_table(self):
        return self.__routing_table

    def add_route(self, destination, channel):
        self.__routing_table[destination] = channel

    def set_package(self, package):
        self.packages.append(package)



    def route(self, destination):
        if destination in self.__routing_table:
            return self.__routing_table[destination]
        else:
            return "Default Gateway"  # 默认网关


class Channel:
    def __init__(self, name, source, destination, data=""):
        self.__name = str(name)
        self.__source = source
        self.__destination = destination
        self.__data = data

    def __repr__(self):
        return "Channel " + self.__name + ": " + self.__source.get_name() + "->" + self.__destination.get_name() + "  " + self.__data

    def get_name(self):
        return self.__name

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_data(self):
        return self.__data

    def send(self):
        print(f"Sending data from {self.__source} to {self.__destination}: {self.__data}")

    def receive(self):
        print(f"Receiving data at {self.__destination} from {self.__source}: {self.__data}")
