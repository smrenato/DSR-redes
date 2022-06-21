"""


"""

import logging
import os
import sys
from datetime import datetime

sys.path.insert(0,os.path.abspath(os.curdir))

from src.controllers import RequestController, log
from src.data import ReadMessage, readDataFile
from src.physical_layer import Host, Package_ID_Counter


def main() -> None :

    payload = readDataFile("nodes.json")
    nodes = payload[1]
    hosts = []
   

    # Cria os roteadores
    package_ID_Counter = Package_ID_Counter()

    for node in nodes:
        host = Host(node, master, package_ID_Counter)
        hosts.append(host)

    messages = ReadMessage("message.json")

    # Adiciona a lista de todos os roteadores no roteador
    for idx in range(len(hosts)):
        hosts[idx].set_hosts(hosts[:idx] + hosts[idx + 1 :])

    time = datetime.now()
    time = time.strftime("%d/%m/%Y %H:%M")

    log(f"========================================= Start in: {time} ================================================")

    count = 1

    for message in messages:
        # Envia a mensagem
        hosts[message.origin].send_message(message.message, message.destiny)

        while master.get_all_requests() != []:

            time = datetime.now()
            time = time.strftime("%d/%m/%Y %H:%M")
            log(f"  {count}. ### Request: {time}")

            master.send_permission()
            count += 1

        time = datetime.now()
        time = time.strftime("%d/%m/%Y %H:%M")

    log(f"\n================================ END: {time}===========================================\n\n")


if __name__ == "__main__":

    logging.basicConfig(filename="logs.log", level=logging.INFO)
    master = RequestController()
    main()
