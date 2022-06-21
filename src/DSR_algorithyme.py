""" DSR algoritimo 

Returns:
    _type_: _description_
"""

from copy import deepcopy

from .controllers import Package, log


class Network:
    def __init__(self, host, package_ID_Counter):
        self.package_id = package_ID_Counter
        self.received_package = []
        self.pending_packages = []
        self.host = host

    def get_next_jump(self, hosts):

        for idx, host in enumerate(hosts):
            if host.node.id == self.host.node.id:
                return hosts[idx + 1]

    def add_received_package(self, package_id):
        if package_id in self.received_package:
            return False

        self.received_package.append(package_id)
        return True

    def send_package(self, message: str, destination: int):

        if message:
            package = Package(
                self.package_id.get(), "DATA", message, self.host.node.id, destination
            )

            log(
                f"NETWORK: Create packge DATA from Host[{self.host.node.id}] To Destiny Host[{destination}]"
            )
            self.package_id.add()

            self.host.set_neighbours()

            for host in self.host.neighbours:
                if destination == host.node.id:
                    log(f"NETWORK: Host[{destination}] is neighbor")
                    self.host.link.sending_request(package)
                    return

            if self.host.check_destiny(destination):
                hosts = self.host.routes[destination]
                log(
                    f"NETWORK: Host[{self.host.node.id}] can reach the destiny"
                )
                package.path = hosts
                package.next = self.get_next_jump(hosts)
                log(
                    f"NETWORK: Sending DATA to the next Host[{package.next.node.id}]"
                )

                self.host.link.sending_request(package)

            else:
                log(
                    f"NETWORK: Host[{self.host.node.id}] Don't have route to Host[{destination}]"
                )
                self.pending_packages.append(package)

                package_RREQ = Package(
                    self.package_id.get(),
                    "RREQ",
                    "",
                    self.host.node.id,
                    package.destiny,
                )
                self.package_id.add()

                self.received_package.append(package_RREQ.id)
                log(
                    f"NETWORK: Host[{self.host.node.id}] creating RREQ to Host[{destination}]"
                )
                log(
                    f"NETWORK: Host[{self.host.node.id}] adding path"
                )

                package_RREQ.path.append(self.host)
                self.host.link.sending_request(package_RREQ)

    def receive_package(self, package: Package):
        log(f" NETWORK: Receive |{package.type}| by the enlance.")
        if package.type == "DATA":
            self.receive_data_package(package)
        elif package.type == "RREQ":
            self.receive_rreq_package(package)
        else:
            self.receive_rrep_package(package)

    def receive_data_package(self, package: Package):
        package = deepcopy(package)
        if package.destiny == self.host.node.id:
            if self.add_received_package(package.id):
                log(
                    f"NETWORK: Host[{self.host.node.id}] receive a package from Host[{package.origin}]\n"
                    + f" message is: {package.content}."
                )

        elif package.next != None and self.host.node.id == package.next.node.id:
            log(
                f"NETWORK: Host[{self.host.node.id}] receive package DATA, But I am not the Receiver"
            )
            if self.add_received_package(package.id):
                package.next = self.get_next_jump(package.path)
                log(
                    f"NETWORK: Send DATA to the next Host[{package.next.node.id}]"
                )

                self.host.link.sending_request(package)

    def receive_rreq_package(self, package: Package):
        package = deepcopy(package)
        if self.host.node.id == package.destiny:
            if self.add_received_package(package.id):
                package.path.append(self.host)

                package_RREP = Package(
                    self.package_id.get(), "RREP", "", self.host.node.id, package.origin
                )
                log(
                    f"NETWORK: Host[{self.host.node.id}] Receive a package RREQ, it's Receiver"
                )
                log(
                    f"NETWORK: Host[{self.host.node.id}] Sending a package RREP to Host[{package.origin}]"
                )

                self.package_id.add()

                package_RREP.path = package.path
                self.host.routes[package.origin] = package.path[::-1]
                package_RREP.next = self.host.routes[package.origin][1]

                self.host.link.sending_request(package_RREP)

        else:
            if self.add_received_package(package.id):
                log(
                    f"NETWORK: Host[{self.host.node.id}] receive RREQ, but I am not the  Host destiny"
                )
                log(
                    f"NETWORK: Host[{self.host.node.id}] sending a pakage  broadcast RREQ"
                )
                log(
                    f"NETWORK: Host[{self.host.node.id}] adding a path"
                )

                package.path.append(self.host)
                self.host.link.sending_request(package)

    def receive_rrep_package(self, package: Package):
        package = deepcopy(package)
        if self.host.node.id == package.destiny:
            if self.add_received_package(package.id):
                log(
                    f"NETWORK: Host[{self.host.node.id}] receive a pakage RREP of Host[{package.origin}]"
                )
                log(
                    f"NETWORK: , e estou enviando pacote de dados para Hospedeiro[{package.origin}]"
                )

                data_package = self.pending_packages.pop(0)
                paths = deepcopy(package.path)
                while len(paths) > 2:
                    self.host.routes[paths.pop().node.id] = package.path

                next_host = package.path.index(package.next) + 1
                data_package.next = package.path[next_host]
                data_package.path = package.path
                log(
                    f"     Rede: Estou enviando DATA para o próximo Hospedeiro[{data_package.next.node.id}]"
                )

                self.host.link.sending_request(data_package)

        elif self.host.node.id == package.next.node.id:
            if self.add_received_package(package.id):
                next_host = package.path.index(package.next) - 1

                package.next = package.path[next_host]
                log(
                    f"     Rede: Hospedeiro[{self.host.node.id}] Recebi um pacote da RREP, mas não sou o destinatário"
                )
                log(
                    f"     Rede: Estou enviando RREP para o próximo Hospedeiro[{package.next.node.id}]"
                )
                self.host.link.sending_request(package)
