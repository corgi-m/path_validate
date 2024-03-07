import os
import random

from Crypto.Cipher import AES

from config.config import init
from generate.package_generate import package_generate
from generate.route_generate import route_generate
from generate.topology_generate import topology_generate
from model.Destination import Destinsation
from model.Network import Network
from model.Package import OPTPackage
from model.Route import Route
from model.Source import Source
from tools.crypto import calc_md5, calc_hmac

if __name__ == "__main__":
    init('config/config.ini')
    G = topology_generate(int(os.getenv('NodeNum')))
    ROUTE = route_generate(G, int(os.getenv('RouteNum')))
    # draw_topology(G, ROUTE)
    net = Network()
    net.set_network(G)
    nodes_dict = net.get_nodes()
    edges_dict = net.get_edges()
    H = calc_md5
    MAC = calc_hmac
    for route in ROUTE:
        # source = type(Source)(nodes_dict[route[0]])
        # destination = type(Destinsation)(nodes_dict[route[-1]])
        # Routei = [type(Route)(nodes_dict[i]) for i in route[1:-1]]
        print(route)
        source = nodes_dict[route[0]]
        destination = nodes_dict[route[1]]
        routei = [nodes_dict[i] for i in route[2][1:-1]]
        # 密钥初始化
        Ki = []
        for i in routei:
            key = random.randbytes(32)
            Ki.append(key)
            #aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        Kd = random.randbytes(32)

        package = package_generate(H, MAC, source.PK, routei, Ki, Kd)

        print(package)