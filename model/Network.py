import os
import random
import time
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor

from model.Package import OPTPackage
from model.RSAManager import RSAManager
from tools.strtool import strcat


class Network:
    instance = None

    def __init__(self, ):
        self.__nodes = {}
        self.__edges = {}

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def set_network(self, G):
        for node_index in G.nodes:
            self.__nodes[node_index] = Node(node_index)

        edge_index = 0
        for edge in G.edges:
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[0]], self.__nodes[edge[1]])
            self.__nodes[edge[0]].add_route(self.__nodes[edge[1]], self.__edges[edge_index])
            edge_index += 1
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[1]], self.__nodes[edge[0]])
            self.__nodes[edge[1]].add_route(self.__nodes[edge[0]], self.__edges[edge_index])
            edge_index += 1

    def get_nodes(self):
        return self.__nodes

    def get_node(self, id):
        return self.__nodes[id]

    def get_edges(self):
        return self.__edges

    def get_edge(self, id):
        return self.__edges[id]

    def init_package(self, ROUTE):
        for route in ROUTE:
            source = self.get_node(route[0])
            destination = self.get_node(route[-1])
            PATH = [self.get_node(i) for i in route]

            package = OPTPackage()
            payload = self.gen_payload()
            Ki = self.gen_Ki(package, source, destination, PATH)
            package.initialization(PK=source.PK, Ki=Ki, PATH=PATH, payload=payload)
            source.add_package(package)

    def do(self, i):
        i.forward()

    def network_start(self):
        with ThreadPoolExecutor(max_workers=len(self.__nodes)) as executor:
        #with ThreadPoolExecutor(max_workers=1) as executor:
            results = executor.map(self.do, list(self.__nodes.values()))
        executor.shutdown(wait=True)
        for result in results:
            print(1)
        #self.do(list(self.__nodes.values())[0])

    def gen_payload(self, size=1):
        size = random.randint(1, 65535) if size is None else size
        payload = random.randbytes(size)
        return payload

    def gen_Ki(self, package, source, destination, PATH):
        Ki = []
        for i in PATH:
            key = random.randbytes(32)
            Ki.append(key)  # aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        for i in range(len(Ki)):
            source.add_Ki(package, PATH[i], Ki[i])
            destination.add_Ki(package, PATH[i], Ki[i])
            PATH[i].add_Ki(package, source, Ki[i])
        return Ki


class Node:
    def __init__(self, id):
        self.__id = id
        self.__routing_table = {}  # 路由表
        self.packages = []
        self.Ki = {}
        (self.SK, self.PK) = RSAManager.load_keys(os.getenv('RandomSeed'), self.__id)

    def __repr__(self):
        return strcat("Node ", self.__id)

    def __eq__(self, other):
        return self.__id == other.get_id()

    def __hash__(self):
        return hash(self.__id)

    def get_id(self):
        return self.__id

    def get_routing_table(self):
        return self.__routing_table

    def add_route(self, destination, channel):
        self.__routing_table[destination] = channel

    def add_package(self, package):
        self.packages.append(package)

    def add_Ki(self, package, node, Ki):
        # logging.debug(Ki)
        if package not in self.Ki:
            self.Ki[package] = {}
        self.Ki[package][node] = Ki

    def receive(self, package):
        PATH = package.get_path()
        I = PATH.index(self)
        source = PATH[0]
        destination = PATH[-1]
        if I == len(PATH) - 1:
            Ki = [self.Ki[package][i] for i in PATH[1:-1]]
            Kd = self.Ki[package][destination]
            if True or package.D_validation(Ki, Kd):
                self.succeed(package)
            else:
                self.drop()
        else:
            if True or package.R_validation(self.Ki[package][source], I):
                self.process(package)
            else:
                self.drop()

    def forward(self):
        while True:
            if len(self.packages) != 0:
                package = self.packages[0]
                self.packages = self.packages[1:]
                PATH = package.get_path()
                I = PATH.index(self)
                R_next = PATH[I + 1]
                Channel = self.__routing_table[R_next]
                Channel.transfer(package)


    def drop(self):
        ...

    def succeed(self, package):
        print(strcat(package.get_path(),'finish'))

    def process(self, package):
        self.packages.append(package)


class Channel:
    def __init__(self, id, source, destination, data=""):
        self.__id = str(id)
        self.__source = source
        self.__destination = destination
        self.__data = data

    def __repr__(self):
        return strcat("Channel ", self.__id, ': ', self.__source, ' -> ', self.__destination)

    def get_id(self):
        return self.__id

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_data(self):
        return self.__data

    def transfer(self, package):
        self.__destination.receive(package)
        return
