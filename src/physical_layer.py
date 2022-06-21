import numpy as np

from .controllers import Link, Node, RequestController, log
from .DSR_algorithyme import Network


class Physical:
    def __init__(self, host):
        self.host = host

    def send_package(self, package):
        self.host.set_neighbours()
        neighbours = self.host.neighbours

        for neighbour in neighbours:
            log(
                f"     Camada Física: Hospedeiro[{self.host.node.id}] enviando pacote para Hospedeiro[{neighbour.node.id}]"
            )
            neighbour.physical.receive_package(package)

    def receive_package(self, package):
        self.host.link.receive_package_to_physical(package)


class Host:
    def __init__(
        self, node: Node, requestController: RequestController, package_ID_Counter
    ):
        self.node = node
        self.requestController = requestController
        self.network = Network(self, package_ID_Counter)
        self.link = Link(self)
        self.physical = Physical(self)
        self.hosts = []
        self.routes = {}
        self.neighbours = set()

    def set_hosts(self, hosts):
        self.hosts: list[self] = hosts

    def send_message(self, message: str, destination: int):
        self.network.send_package(message, destination)

    def check_destiny(self, destiny: int):
        return destiny in self.routes

    def set_neighbours(self):
        origin_node_axis = np.array((self.node.position["x"], self.node.position["y"]))

        for host in self.hosts:
            destiny_node_axis = np.array(
                (host.node.position["x"], host.node.position["y"])
            )
            node_distance = np.linalg.norm(origin_node_axis - destiny_node_axis)

            if node_distance < self.node.radius:
                self.neighbours.add(host)


class Package_ID_Counter:
    def __init__(self):
        self.package_id = 0

    def add(self):
        self.package_id += 1

    def get(self):
        return self.package_id

