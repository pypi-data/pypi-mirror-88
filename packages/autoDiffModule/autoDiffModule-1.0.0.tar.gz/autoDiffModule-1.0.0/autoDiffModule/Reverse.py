import numpy as np
import math

class TableReverseVector:
    def __init__(self, num_inputs):
        self.table = list()
        for i in range(num_inputs):
            self.table.append(TableReverse())
        self.val = None
        self.der = None

    def generate_derivatives(self):
        self.val = list()
        self.der = list()
        for table in self.table:
            table.generate_derivatives()
            print("TYPE {}".format(type(table.der[0])))
            self.der.append(table.der[0])
            #print(table.der[0])
            self.val.append(table.val)


class NodeVector:

    def __init__(self, input, tableVector, initialization=True):
        self.table = tableVector
        if initialization:
            self.nodes = list()
            for i in range(len(input)):
                self.nodes.append(Node(value=input[i], table=self.table.table[i]))
        else:
            self.nodes = input

    def __eq__(self, other):
        try:
            return self.nodes == other.nodes
        except AttributeError:
            return self.nodes == other

    def __ne__(self, other):
        try:
            return self.nodes != other.nodes
        except AttributeError:
            return self.nodes != other

    def __add__(self, other):
        try:
            return NodeVector(input=[self.nodes[i] + other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node + other for node in self.nodes], tableVector=self.table, initialization=False)

    def __sub__(self, other):
        try:
            return NodeVector(input=[self.nodes[i] - other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node - other for node in self.nodes], tableVector=self.table, initialization=False)

    def __mul__(self, other):
        try:
            return NodeVector(input=[self.nodes[i] * other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node * other for node in self.nodes], tableVector=self.table, initialization=False)

    def __truediv__(self, other):
        try:
            return NodeVector(input=[self.nodes[i] / other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node / other for node in self.nodes], tableVector=self.table, initialization=False)

    def __pow__(self, other):
        try:
            return NodeVector(input=[self.nodes[i] ** other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node ** other for node in self.nodes], tableVector=self.table, initialization=False)

    def __neg__(self):
        return NodeVector(input=[-self.nodes[i] for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def __pos__(self):
        return NodeVector(input=[self.nodes[i] for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

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
        pass

    def sin(self):
        return NodeVector(input=[self.nodes[i].sin() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def cos(self):
        return NodeVector(input=[self.nodes[i].cos() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def tan(self):
        return NodeVector(input=[self.nodes[i].tan() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arcsin(self):
        return NodeVector(input=[self.nodes[i].arcsin() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arccos(self):
        return NodeVector(input=[self.nodes[i].arccos() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arctan(self):
        return NodeVector(input=[self.nodes[i].arctan() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def sinh(self):
        return NodeVector(input=[self.nodes[i].sinh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def cosh(self):
        return NodeVector(input=[self.nodes[i].cosh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def tanh(self):
        return NodeVector(input=[self.nodes[i].tanh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def logistic(self):
        return NodeVector(input=[self.nodes[i].logistic() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def exp(self):
        return NodeVector(input=[self.nodes[i].exp() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def log(self):
        return NodeVector(input=[self.nodes[i].log() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def sqrt(self):
        return NodeVector(input=[self.nodes[i].sqrt() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)


class TableReverse:

    def __init__(self):
        self.nodes = list()
        self.der = list()
        self.size=0
        self.val = None

    def generate_derivatives(self):
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
                self.der.append(node.derivative)
        # print(type(node.derivative))
        # print(node.derivative)
        # print(self)

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
        self.node_number = self.table.size - 1
        self.derivative = 0

    def __eq__(self, other):
        try:
            return self.val == other.val and self.der == self.der
        except AttributeError:
            return self.val == other

    def __ne__(self, other):
        try:
            return self.val != other.val or self.der != other.der
        except AttributeError:
            return self.val != other

    def __repr__(self):
        return "=====NODE=====\nNODE: {}, VALUE: {}, PARTIAL DERIVATIVES: {}, BAR DERIVATIVE: {}\n=====NODE=====".format(self.node_number, self.val, self.partial_derivatives, self.derivative)

    def __add__(self, other):
        try:
            return Node(value=self.val + other.val, partial_derivatives={self.node_number: 1, other.node_number: 1}, table=self.table)
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
            return Node(value=self.val / other.val, partial_derivatives={self.node_number: 1/other.val, other.node_number: -self.val / other.val**2}, table=self.table)
        except AttributeError:
            return Node(value=self.val / other, partial_derivatives={self.node_number: 1/other}, table=self.table)

    def __pow__(self, other):
        try:
            return Node(value=self.val ** other.val, partial_derivatives={self.node_number: other.val * self.val**(other.val-1), other.node_number: self.val**other.val * math.log(self.val)}, table=self.table)
        except AttributeError:
            return Node(value=self.val ** other, partial_derivatives={self.node_number: other * self.val**(other-1)}, table=self.table)

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
        return Node(value=math.tan(self.val), partial_derivatives={self.node_number: 1/math.cos(self.val)**2}, table=self.table)

    def arcsin(self):
        return Node(value=math.asin(self.val), partial_derivatives={self.node_number: 1/(1 - self.val**2)**0.5}, table=self.table)

    def arccos(self):
        return Node(value=math.acos(self.val), partial_derivatives={self.node_number: -1/(1 - self.val**2)**0.5}, table=self.table)

    def arctan(self):
        return Node(value=math.atan(self.val), partial_derivatives={self.node_number: 1/(1 + self.val**2)}, table=self.table)

    def sinh(self):
        return Node(value=math.sinh(self.val), partial_derivatives={self.node_number: math.cosh(self.val)}, table=self.table)

    def cosh(self):
        return Node(value=math.cosh(self.val), partial_derivatives={self.node_number: math.sinh(self.val)}, table=self.table)

    def tanh(self):
        return Node(value=math.tanh(self.val), partial_derivatives={self.node_number: 1 - math.tanh(self.val)**2}, table=self.table)

    def logistic(self):
        return Node(value=1 / (1 + math.exp(-self.val)), partial_derivatives={self.node_number: (math.exp(-self.val)) / (1 + math.exp(-self.val))**2}, table=self.table)

    def exp(self):
        return Node(value=math.exp(self.val), partial_derivatives={self.node_number: math.exp(self.val)}, table=self.table)

    def log(self, base=math.e):
        return Node(value=math.log(self.val, base), partial_derivatives={self.node_number: 1/(self.val*math.log(base))}, table=self.table)

    def sqrt(self):
        return Node(value=self.val**0.5, partial_derivatives={self.node_number: 1/(2*self.val**0.5)}, table=self.table)

