import logging
import os
import time

from config.config import init
from controller.GenFactory import GenFactory
from model.Network import Network
from tools.tools import strcat, load_obj

if __name__ == "__main__":
    init('config/config.ini')
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(strcat('gen_G start ', time.time()))
    G = load_obj('record/graph', os.getenv('RandomSeed'), 'graph', GenFactory.gen_topology)
    logging.debug(strcat('gen_ROUTE start ', time.time()))
    ROUTE = load_obj('record/route', os.getenv('RandomSeed'), 'route', GenFactory.gen_route, G=G,
                     num_paths_to_select=int(os.getenv('RouteNum')))
    logging.debug(strcat('gen_ROUTE end ', time.time()))
    net = Network(G, ROUTE)
    net.network_start()  # logging.debug(f'{OPTPackage.packages[0]}')
