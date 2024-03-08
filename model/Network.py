import os
from concurrent.futures import ThreadPoolExecutor

from model.GenFactory import GenFactory
from model.Package import OPTPackage
from model.RSAManager import RSAManager
from tools.tools import strcat


class Network:
    instance = None
    incomplete = 0

    def __init__(self, G, ROUTE):
        self.__nodes = {}
        self.__edges = {}
        self.G = G
        self.ROUTE = ROUTE
        self.set_incomplete(len(ROUTE))
        self.init_network()
        self.init_package()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init_network(self):
        for node_index in self.G.nodes:
            self.__nodes[node_index] = Node(node_index)

        edge_index = 0
        for edge in self.G.edges:
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[0]], self.__nodes[edge[1]])
            self.__nodes[edge[0]].add_route(self.__nodes[edge[1]], self.__edges[edge_index])
            edge_index += 1
            self.__edges[edge_index] = Channel(edge_index, self.__nodes[edge[1]], self.__nodes[edge[0]])
            self.__nodes[edge[1]].add_route(self.__nodes[edge[0]], self.__edges[edge_index])
            edge_index += 1

    def init_package(self):
        for route in self.ROUTE:
            source = self.get_node(route[0])
            destination = self.get_node(route[-1])
            PATH = [self.get_node(i) for i in route]

            package = OPTPackage()
            payload = GenFactory.gen_payload()
            Ki = GenFactory.gen_Ki(package, source, destination, PATH)
            package.initialization(PK=source.PK, Ki=Ki, PATH=PATH, payload=payload)
            source.add_package(package)

    def network_start(self):
        do = lambda x: x.forward()
        with ThreadPoolExecutor(max_workers=len(self.__nodes)) as executor:
            results = executor.map(do, list(self.__nodes.values()))
        executor.shutdown(wait=True)

    @classmethod
    def complete(cls):
        cls.incomplete -= 1
        return cls.incomplete

    @classmethod
    def is_complete(cls):
        if cls.incomplete == 0:
            return True
        else:
            return False

    def get_nodes(self):
        return self.__nodes

    def get_node(self, id):
        return self.__nodes[id]

    def get_edges(self):
        return self.__edges

    def get_edge(self, id):
        return self.__edges[id]

    @classmethod
    def set_incomplete(cls, param):
        cls.incomplete = param


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
                self.drop(package)
        else:
            if True or package.R_validation(self.Ki[package][source], I):
                self.process(package)
            else:
                self.drop(package)

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
            if Network.is_complete():
                break

    def drop(self, package):
        leave = Network.complete()
        print(strcat(package.get_path(), 'drop', 'Network leave:', leave))

    def succeed(self, package):
        leave = Network.complete()
        print(strcat(package.get_path(), 'finish', 'Network leave:', leave))

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
