import json
from pprint import pprint

from opcode import opname

from src.controllers import Message, Node

# def read_data_file(path: str) -> tuple:
#     nodes = []

#     with open(path, "r") as configs:
#         data = json.load(configs)

#     for node_raw in data["nodes"]:
#         print(node_raw)
#         nodes.append(
#             Node(node_raw["node_id"], node_raw["x"], node_raw["y"], node_raw["radius"])
#         )

#     return (
#         data["number_of_nodes"],
#         nodes,
#         data["min_xy"],
#         data["min_xy"],
#         data["max_xy"],
#         data["max_xy"],
#     )


# print(read_data_file("nodes.json"))



ReadMessage("menssage.json")
