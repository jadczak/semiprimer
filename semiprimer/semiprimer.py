from collections import namedtuple, deque
from typing import Union

Node = namedtuple("Node", ["a", "b", "level"])


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

    def factor(self):
        self.initialize_node_list()
        nodes_processed = 0
        while self.nodes:
            node = self.nodes.popleft()
            if node.a * node.b == self.semiprime_int and node.a != 1 and node.b != 1:
                self.factors = (node.a, node.b)
                print("SUCCESS")
                print(f"Semiprime:\t{self.semiprime_string}")
                print(f"A Factor:\t{node.a}")
                print(f"B Factor:\t{node.b}")
                break
            new_nodes = self.process_node(node)
            self.nodes.extend(new_nodes)
            nodes_processed = nodes_processed + 1
            if nodes_processed % 5000 == 0:
                print(f"Nodes Processed: {nodes_processed}")
                print(f"Node List Length: {len(self.nodes)}")
                print(f"Most Recent Node: a={node.a}, b={node.b}, level={node.level}")

    def initialize_node_list(self):
        nodes = self.sub_factor(target=self.semiprime_string[-1:])
        self.nodes.extend(nodes)

    def process_node(self, node: Node):
        new_level = node.level + 1
        new_target = self.semiprime_string[-new_level:]
        return self.sub_factor(target=new_target, level=new_level, a_value=node.a, b_value=node.b)

    @staticmethod
    def sub_factor(target: str, level: int = 1, a_value: int = 0, b_value: int = 0):
        ab_pairs = set()
        for a in range(10):
            for b in range(10):
                current_a = a_value + a * 10 ** (level - 1)
                current_b = b_value + b * 10 ** (level - 1)
                current_product = current_a * current_b
                current_product_string = str(current_product)
                if current_product_string[-level:] == target:
                    ab = (current_a, current_b)
                    ab_pairs.add(Node(a=min(ab), b=max(ab), level=level))
        return ab_pairs
