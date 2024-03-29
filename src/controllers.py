"""_summary_

Returns:
    _type_: _description_
"""
import logging


def log(message: str):
    logging.info(message)
    print(message)


class Package_ID_Counter:
    def __init__(self):
        self.package_id = 0

    def add(self):
        self.package_id += 1

    def get(self):
        return self.package_id


class Message:
    def __init__(self, message: str, origin: int, destiny: int):
        self.message = message
        self.origin = origin
        self.destiny = destiny


class RequestController:
    def __init__(self):
        self.envia_fila = []
        self.remetente_permitido = None
        self.remetente_permitido = None

    def send_permission(self):
        if len(self.envia_fila) > 0:
            self.remetente_permitido = self.envia_fila.pop(0)

            log(
                f"     Controlador de Requisições: Hospedeiro[{self.remetente_permitido.node.id}] tem permissão para começar a enviar"
            )

            self.remetente_permitido.link.send_package_to_physical()
        else:
            log(
                f"  Controlador de Requisições: não há Hospedeiros na fila para enviar\n"
            )

    def add_queue(self, host):
        log(
            f"     Controlador de Requisições: o Hospedeiro[{host.node.id}] deseja enviar um pacote e espera a permissão.\n"
        )
        self.envia_fila.append(host)

    def get_all_requests(self):
        return self.envia_fila


class Node:
    def __init__(self, node_id: int, x: int, y: int, radius: float):
        self.id = node_id
        self.position = {"x": x, "y": y}
        self.radius = radius


class Link:
    def __init__(self, host):
        self.host = host
        self.pending_package = []
        self.package = 0

    def sending_request(self, package):
        self.pending_package.append(package)
        log(
            f"     Camada de Enlace: Enviando pacote do Hospedeiro para o controlador de solicitação[{self.host.node.id}]"
        )
        self.host.requestController.add_queue(self.host)

    def send_package_to_physical(self):
        self.package = self.pending_package.pop(0)
        self.host.physical.send_package(self.package)

    def receive_package_to_physical(self, package):
        log(
            f"     Camada de Enlace: Recebe o pacote |{package.type}| da Camada Física e envie para a Camada de Rede"
        )
        self.host.network.receive_package(package)


class Package:
    def __init__(
        self,
        package_id: int,
        package_type: str,
        content: str,
        origin: int,
        destiny: int,
    ):
        self.id = package_id
        self.type = package_type
        self.content = content
        self.origin = origin
        self.destiny = destiny
        self.next = None
        self.path = []

