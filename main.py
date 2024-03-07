import logging
import os

from config.config import init
from generate.route_generate import route_generate
from generate.topology_generate import topology_generate
from model.Network import Network

if __name__ == "__main__":
    init('config/config.ini')
    logging.basicConfig(level=logging.DEBUG)
    G = topology_generate(int(os.getenv('NodeNum')))
    ROUTE = route_generate(G, int(os.getenv('RouteNum')))
    # draw_topology(G, ROUTE)
    net = Network()
    net.set_network(G)
    #print(net.get_nodes())
    #print(net.get_edges())
    net.init_package(ROUTE)
    net.network_start()
    # logging.debug(f'{OPTPackage.packages[0]}')
