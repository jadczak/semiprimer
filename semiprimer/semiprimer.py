from collections import namedtuple, deque
from typing import Union


class SemiPrime:
    def __init__(self, semiprime: Union[str, int, float]):
        if isinstance(semiprime, int):
            self.semiprime_string = str(semiprime)
            self.semiprime_int = semiprime
        elif isinstance(semiprime, float):
            self.semiprime_string = str(int(semiprime))
            self.semiprime_int = int(semiprime)
        elif isinstance(semiprime, str):
            self.semiprime_string = semiprime
            self.semiprime_int = int(semiprime)
        else:
            raise TypeError(f"Expecting str, float, or int.  Instead got {type(semiprime)}")
        self.solved = False
        self.factors = None
        self.nodes = deque()
        self.truncated_semi_lookup = {
            i + 1: self.semiprime_int % 10 ** (i + 1) for i in range(len(self.semiprime_string))
        }
        self.a = 0
        self.b = 1
        self.level = 2

    def factor(self):
        self.initialize_node_list()
        nodes_processed = 0
        nodes_rejected = 0
        while self.nodes:
            node = self.nodes.pop()
            ab_product = node[self.a] * node[self.b]
            if ab_product == self.semiprime_int and node[self.a] != 1 and node[self.b] != 1:
                self.factors = (node[self.a], node[self.b])
                self.solved = True
                print("SUCCESS")
                print(f"Semiprime:\t{self.semiprime_string}")
                print(f"A Factor:\t{node[self.a]}")
                print(f"B Factor:\t{node[self.b]}")
                print(f"Nodes Processed:\t{nodes_processed}")
                print(f"Nodes Rejected:\t{nodes_rejected}")
                return
            elif ab_product > self.semiprime_int or (
                ab_product == self.semiprime_int and (node[self.a] == 1 or node[self.b] == 1)
            ):
                nodes_rejected += 1
                continue
            new_nodes = self.process_node(node)
            self.nodes.extend(new_nodes)
            nodes_processed = nodes_processed + 1
            if nodes_processed % 25000 == 0:
                print(f"Nodes Processed:  {nodes_processed}")
                print(f"Nodes Rejected:   {nodes_rejected}")
                print(f"Node List Length: {len(self.nodes)}")
                print(f"Most Recent Node: a={node[self.a]}, b={node[self.b]}, level={node[self.level]}\n")
        if not self.solved:
            raise (ValueError(f"Could not find factors for {self.semiprime_string}.  Prime?"))

    def initialize_node_list(self):
        nodes = self.sub_factor(target=self.truncated_semi_lookup[1])
        self.nodes.extend(nodes)

    def process_node(self, node: tuple):
        new_level = node[self.level] + 1
        truncator = 10 ** new_level
        new_target = self.truncated_semi_lookup[new_level]
        return self.sub_factor(
            target=new_target, level=new_level, a_value=node[self.a], b_value=node[self.b], truncator=truncator
        )

    @staticmethod
    def sub_factor(target: int, level: int = 1, a_value: int = 0, b_value: int = 0, truncator: int = 10):
        ab_pairs = set()
        scale = 10 ** (level - 1)
        for a in range(10):
            current_a = a_value + a * scale
            for b in range(10):
                current_b = b_value + b * scale
                current_product = current_a * current_b
                current_truncated_product = current_product % truncator
                if current_truncated_product == target:
                    if current_a > current_b:
                        current_a, current_b = current_b, current_a
                    ab_pairs.add((current_a, current_b, level))
        return ab_pairs
