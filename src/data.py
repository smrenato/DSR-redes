"""


"""
import csv
import json

from .controllers import Message, Node

def readDataFile(input_file_path: str):
    nodes = []
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        number_of_nodes = int(lines[2])
        min_x, min_y = int(lines[0]), int(lines[0])
        max_x, max_y = int(lines[1]), int(lines[1])
        
        for node_id, node in enumerate(lines[3:]):
            x, y, radius = node.split(' ')
            nodes.append(Node(node_id, int(x), int(y), float(radius)))

    return number_of_nodes, nodes, min_x, min_y, max_x, max_y


def ReadMessage(path: str) -> Message:
    messages = []

    with open(path, "r") as menssgens_file:
        payload = json.load(menssgens_file)

    for msg in payload:
        
        messages.append(Message(msg["menssage"], msg["host_send"], msg["host_receive"]))

    return messages

