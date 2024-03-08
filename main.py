import logging
import os

from config.config import init
from model.GenFactory import GenFactory
from model.Network import Network

if __name__ == "__main__":
    init('config/config.ini')
    logging.basicConfig(level=logging.DEBUG)
    G = GenFactory.gen_topology(int(os.getenv('NodeNum')))
    ROUTE = GenFactory.gen_route(G, int(os.getenv('RouteNum')))
    net = Network(G, ROUTE)
    net.network_start()  # logging.debug(f'{OPTPackage.packages[0]}')
