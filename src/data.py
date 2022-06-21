"""


"""
import csv
import json

from .controllers import Message, Node


def readDataFile(path: str) -> tuple:
    nodes = []

    with open(path, "r") as configs:
        data = json.load(configs)

    for node_raw in data["nodes"]:
        nodes.append(
            Node(node_raw["node_id"], node_raw["x"], node_raw["y"], node_raw["radius"])
        )

    return (
        data["number_of_nodes"],
        nodes,
        data["min_xy"],
        data["min_xy"],
        data["max_xy"],
        data["max_xy"],
    )


def ReadMessage(path: str) -> Message:
    messages = []

    with open(path, "r") as menssgens_file:
        payload = json.load(menssgens_file)

    for msg in payload:
        
        messages.append(Message(msg["menssage"], msg["host_send"], msg["host_receive"]))

    return messages

