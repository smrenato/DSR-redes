import json
from random import randint

node = {"node_id": 1, "x": 0, "y": 0, "radius": 3}

NUMBER_OF_NODES = 10

def main(path: str, n_nodes : int , set_min_xy: int, set_max_xy: int) -> None:
    
    with open(path, "r") as configs:
        data = json.load(configs)

    number_of_nodes =  data["number_of_nodes"]
    min_xy =  data["min_xy"]
    max_xy =  data["max_xy"]

    for n in range(n_nodes):
        number_of_nodes += 1
        data["nodes"].append(
            {
                "node_id":  number_of_nodes,
                "x": randint(set_min_xy, set_max_xy), 
                "y": randint(set_min_xy, set_min_xy), 
                "radius": int((set_min_xy/set_min_xy)*number_of_nodes)

            }
        )

    # # for n in range(NUMBER_OF_NODES):
    # with open(path, "w") as write_file:
    #     json.dump(data, write_file)

if __name__ == "__main__":
    main()
