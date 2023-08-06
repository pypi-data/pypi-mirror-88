import numpy as np
import math


class Table:

    def __init__(self):
        self.nodes = list()
        self.derivative = list()
        self.size=0
        self.val = None

    def generate_derivatives(self):
        print("---{}".format(self.val))
        self.val = self.nodes[-1].val
        visited_nodes = list()
        current_node_index = self.size - 1
        while current_node_index >= 0:
            node = self.nodes[current_node_index]
            if current_node_index == self.size - 1:
                node.derivative += 1
            else:
                if node.node_number not in visited_nodes:
                    for child in node.children:
                        child_node = self.nodes[child]
                        node.derivative += child_node.derivative * child_node.partial_derivatives[node.node_number]

            if node.partial_derivatives:
                for derivative in node.partial_derivatives:
                    parent_node = self.nodes[derivative]
                    parent_node.children.append(node.node_number)

            visited_nodes.append(node.node_number)
            current_node_index -= 1

        for node in self.nodes:
            if not node.partial_derivatives:
                self.derivative.append(node.derivative)

    def __repr__(self):
        output = "=====TABLE====="
        for node in self.nodes:
            output += "\nNODE: {}, VALUE: {}, PARTIAL DERIVATIVES: {} BAR DERIVATIVE: {}".format(node.node_number, node.val, node.partial_derivatives, node.derivative)
        return output + "\n=====TABLE====="


class Node:

    def __init__(self, value, table, partial_derivatives=None):
        self.table = table
        self.val = value
        self.partial_derivatives = partial_derivatives  # dict {node_name
        self.children = list()
        self.table.nodes.append(self)
        self.table.size += 1
        self.node_number = self.table.nodes.index(self)
        self.derivative = 0

    def __repr__(self):
        return "=====NODE=====\nNODE: {}, VALUE: {}, PARTIAL DERIVATIVES: {}, BAR DERIVATIVE: {}\n=====NODE=====".format(self.node_number, self.val, self.partial_derivatives, self.derivative)

    def __add__(self, other):
        try:
            current_value = self.val + other.val
            return Node(value=current_value, partial_derivatives={self.node_number: 1, other.node_number: 1}, table=self.table)
        except AttributeError:
            return Node(value=self.val + other, partial_derivatives={self.node_number: 1}, table=self.table)

    def __sub__(self, other):
        try:
            return Node(value=self.val - other.val, partial_derivatives={self.node_number: 1, other.node_number: -1}, table=self.table)
        except AttributeError:
            return Node(value=self.val - other, partial_derivatives={self.node_number: 1}, table=self.table)

    def __mul__(self, other):
        try:
            return Node(value=self.val * other.val, partial_derivatives={self.node_number: other.val, other.node_number: self.val}, table=self.table)
        except AttributeError:
            return Node(value=self.val * other, partial_derivatives={self.node_number: other}, table=self.table)

    def __truediv__(self, other):
        try:
            return Node(value=self.val / other.val, partial_derivatives={self.node_number: 1/other.val, other.node_number: -self.val / other**2}, table=self.table)
        except AttributeError:
            return Node(value=self.val / other, partial_derivatives={self.node_number: 1/other}, table=self.table)

    def __pow__(self, other):
        pass

    def __neg__(self):
        return Node(value=-self.val, partial_derivatives={self.node_number: -1}, table=self.table)

    def __pos__(self):
        return Node(value=self.val, partial_derivatives={self.node_number: 1}, table=self.table)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        recip_self = self.__pow__(-1.0)
        return recip_self.__mul__(other)

    def __rpow__(self, other):
        return Node(value=other**self.val, partial_derivatives={self.node_number: other**self.val * math.log(other)}, table=self.table)

    def sin(self):
        return Node(value=math.sin(self.val), partial_derivatives={self.node_number: math.cos(self.val)}, table=self.table)

    def cos(self):
        return Node(value=math.cos(self.val), partial_derivatives={self.node_number: -math.sin(self.val)}, table=self.table)

    def tan(self):
        return Node(value=math.tan(self.val), partial_derivatives={self.node_number: 1/math.cos(self.val)}, table=self.table)

    def exp(self):
        return Node(value=math.exp(self.val), partial_derivatives={self.node_number: math.exp(self.val)}, table=self.table)

    def log(self, base=math.e):
        return Node(value=math.log(self.val, base), partial_derivatives={self.node_number: 1/(self.val*math.log(base))}, table=self.table)

    def sqrt(self):
        return Node(value=self.val**2, partial_derivatives={self.node_number: 1/(2*self.val**0.5)}, table=self.table)


def addition_node_test():
    print("\n\n=====ADDITION TEST=====")
    table = Table()
    x_node = Node(value=5, table=table)
    y_node = Node(value=10, table=table)
    function = 5 + x_node + y_node + 3
    print(table)

def multiplication_node_test():
    print("\n\n====MULTIPLICATION TEST=====")
    table = Table()
    x_node = Node(value=5, table=table)
    y_node = Node(value=10, table=table)
    function = x_node * y_node
    print(table)

def addition_table_test():
    print("\n\n=====ADDITION TABLE TEST=====")
    table=Table()
    x_node = Node(value=5, table=table)
    y_node = Node(value=10, table=table)

    function = 5 + x_node + y_node + 3
    print("-after forward pass-")
    print(table)

    table.generate_derivatives()
    print("-after reverse pass-")
    print(table)

    print("FINAL PARTIALS")
    print(table.derivative)

def lecture_example_test():

    print("===== LECTURE EXAMPLE TEST =====")
    print("xy + exp(xy)")
    table = Table()
    x_node = Node(value=1, table=table)
    y_node = Node(value=2, table=table)
    x_node * y_node + (x_node * y_node).exp()
    table.generate_derivatives()
    print(table)
    print("FINAL DERIVATIVES: {}".format(table.derivative))


def main():
    #addition_node_test()
    #multiplication_node_test()
    #addition_table_test()
    lecture_example_test()

if __name__=="__main__":
    main()