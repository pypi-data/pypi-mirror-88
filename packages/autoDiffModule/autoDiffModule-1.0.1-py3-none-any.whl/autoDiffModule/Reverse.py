import numpy as np
import math


class TableReverseVector:
    """Class for storing NodeVector objects. Supports vector input."""
    def __init__(self, num_inputs):
        self.table = list()
        for i in range(num_inputs):
            self.table.append(TableReverse())
        self.val = None
        self.der = None

    def generate_derivatives(self):
        """
        Piecewise generates the derivatives for each TableReverse Object in self.table
        :return:
        """
        self.val = list()
        self.der = list()
        for table in self.table:
            table.generate_derivatives()
            self.der.append(table.der[0])
            self.val.append(table.val)


class NodeVector:
    """
    Class for storing multiple nodes. Supports vector input.
    """

    def __init__(self, input, tableVector, initialization=True):
        self.table = tableVector
        if initialization:
            self.nodes = list()
            for i in range(len(input)):
                self.nodes.append(Node(value=input[i], table=self.table.table[i]))
        else:
            self.nodes = input

    def __eq__(self, other):
        """
        Equal comparison operator.
        :param other: other element in the comparison
        :return:
        """
        try:
            return self.nodes == other.nodes
        except AttributeError:
            return self.nodes == other

    def __ne__(self, other):
        """
        Not equal comparison operator.
        :param other: other element in the comparison
        :return:
        """
        try:
            return self.nodes != other.nodes
        except AttributeError:
            return self.nodes != other

    def __add__(self, other):
        """
        Addition operation for arithmetic involving Node Vector Objects.
        :param other: other element in the operation
        :return: Node Vector representing the sum
        """
        try:
            return NodeVector(input=[self.nodes[i] + other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node + other for node in self.nodes], tableVector=self.table, initialization=False)

    def __sub__(self, other):
        """
        Subtraction operation for arithmetic involving Node Vector Objects.
        :param other: other element in the operation
        :return: Node Vector representing the difference
        """
        try:
            return NodeVector(input=[self.nodes[i] - other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node - other for node in self.nodes], tableVector=self.table, initialization=False)

    def __mul__(self, other):
        """
        Multiplication operation for arithmetic involving Node Vector Objects.
        :param other: other element in the operation
        :return: Node Vector representing the product
        """
        try:
            return NodeVector(input=[self.nodes[i] * other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node * other for node in self.nodes], tableVector=self.table, initialization=False)

    def __truediv__(self, other):
        """
        Division operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node Vector representing the quotient
        """
        try:
            return NodeVector(input=[self.nodes[i] / other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node / other for node in self.nodes], tableVector=self.table, initialization=False)

    def __pow__(self, other):
        """
        Power operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node Vector representing the result
        """
        try:
            return NodeVector(input=[self.nodes[i] ** other.nodes[i] for i in range(len(self.nodes))],
                              tableVector=self.table, initialization=False)
        except AttributeError:
            return NodeVector(input=[node ** other for node in self.nodes], tableVector=self.table, initialization=False)

    def __neg__(self):
        """
        Neg operation for arithmetic involving Node Vector Objects
        :return: Node Vector representing the result
        """
        return NodeVector(input=[-self.nodes[i] for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def __pos__(self):
        """
        Pos operation for arithmetic involving Node Vector Objects
        :return: Node Vector representing the result
        """
        return NodeVector(input=[self.nodes[i] for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def __radd__(self, other):
        """
        Reverse add operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node Vector representing the result
        """
        return self.__add__(other)

    def __rsub__(self, other):
        """
        Reverse subtraction operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node Vector representing the result
        """
        return -self.__sub__(other)

    def __rmul__(self, other):
        """
        Reverse multiplication operation for arithmetic involving Node Vector Objects
        :param other: other element in operation
        :return: Node vector representing the result
        """
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """
        Reverse division operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node Vector representing the result
        """
        recip_self = self.__pow__(-1.0)
        return recip_self.__mul__(other)

    def __rpow__(self, other):
        """
        Reverse power operation for arithmetic involving Node Vector Objects
        :param other: other element in the operation
        :return: Node vector representing the result
        """
        return NodeVector(input=[other.nodes[i]**self.nodes[i] for i in range(len(self.nodes))], tableVector=self.table,
                          initialization=False)

    def sin(self):
        """
        Sin operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].sin() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def cos(self):
        """
        Cos operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].cos() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def tan(self):
        """
        Tan operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].tan() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arcsin(self):
        """
        Arcsin operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].arcsin() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arccos(self):
        """
        Arccos operation for arithemtic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].arccos() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def arctan(self):
        """
        Arctan operation for arithemtic involving Node Vector Objects
        :return: Node Vector representing the result
        """
        return NodeVector(input=[self.nodes[i].arctan() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def sinh(self):
        """
        Sinh operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].sinh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def cosh(self):
        """
        Cosh operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].cosh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def tanh(self):
        """
        Tanh operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].tanh() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def logistic(self):
        """
        Logistic operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].logistic() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def exp(self):
        """
        Exp operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].exp() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def log(self):
        """
        Exp operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].log() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)

    def sqrt(self):
        """
        Sqrt operation for arithmetic involving Node Vector Objects
        :return: Node vector representing the result
        """
        return NodeVector(input=[self.nodes[i].sqrt() for i in range(len(self.nodes))], tableVector=self.table, initialization=False)


class TableReverse:
    """
    Class for storing Node objects. Facilitates reverse pass through the table
    """

    def __init__(self):
        self.nodes = list()
        self.der = list()
        self.size=0
        self.val = None

    def generate_derivatives(self):
        """
        Facilitates reverse pass through the table. Assigns bar derivatives
        :return:
        """
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


    def __repr__(self):
        output = "=====TABLE====="
        for node in self.nodes:
            output += "\nNODE: {}, VALUE: {}, PARTIAL DERIVATIVES: {} BAR DERIVATIVE: {}".format(node.node_number, node.val, node.partial_derivatives, node.derivative)
        return output + "\n=====TABLE====="


class Node:
    """
    Class for storing input variables and intermediate variables.
    """

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
        """
        Equal comparison operator
        :param other: other element in the comparison
        :return:
        """
        try:
            return self.val == other.val and self.der == self.der
        except AttributeError:
            return self.val == other

    def __ne__(self, other):
        """
        Not equal comparison operator
        :param other: other element in the comparison
        :return:
        """
        try:
            return self.val != other.val or self.der != other.der
        except AttributeError:
            return self.val != other

    def __repr__(self):
        return "=====NODE=====\nNODE: {}, VALUE: {}, PARTIAL DERIVATIVES: {}, BAR DERIVATIVE: {}\n=====NODE=====".format(self.node_number, self.val, self.partial_derivatives, self.derivative)

    def __add__(self, other):
        """
        Add operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the sum
        """
        try:
            return Node(value=self.val + other.val, partial_derivatives={self.node_number: 1, other.node_number: 1}, table=self.table)
        except AttributeError:
            return Node(value=self.val + other, partial_derivatives={self.node_number: 1}, table=self.table)

    def __sub__(self, other):
        """
        Subtract operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the difference
        """
        try:
            return Node(value=self.val - other.val, partial_derivatives={self.node_number: 1, other.node_number: -1}, table=self.table)
        except AttributeError:
            return Node(value=self.val - other, partial_derivatives={self.node_number: 1}, table=self.table)

    def __mul__(self, other):
        """
        Multiply operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the product
        """
        try:
            return Node(value=self.val * other.val, partial_derivatives={self.node_number: other.val, other.node_number: self.val}, table=self.table)
        except AttributeError:
            return Node(value=self.val * other, partial_derivatives={self.node_number: other}, table=self.table)

    def __truediv__(self, other):
        """
        Divide operation for arithmetic involving Node Objects.
        :param other: other element in the operation
        :return: Node representing the quotient
        """
        try:
            return Node(value=self.val / other.val, partial_derivatives={self.node_number: 1/other.val, other.node_number: -self.val / other.val**2}, table=self.table)
        except AttributeError:
            return Node(value=self.val / other, partial_derivatives={self.node_number: 1/other}, table=self.table)

    def __pow__(self, other):
        """
        Power operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        try:
            return Node(value=self.val ** other.val, partial_derivatives={self.node_number: other.val * self.val**(other.val-1), other.node_number: self.val**other.val * math.log(self.val)}, table=self.table)
        except AttributeError:
            return Node(value=self.val ** other, partial_derivatives={self.node_number: other * self.val**(other-1)}, table=self.table)

    def __neg__(self):
        """
        Neg operation for arithmetic involving Node Objects
        :return: Node representing the result
        """
        return Node(value=-self.val, partial_derivatives={self.node_number: -1}, table=self.table)

    def __pos__(self):
        """
        Pos operation for arithmetic involving Node Objects
        :return: Node representing the result
        """
        return Node(value=self.val, partial_derivatives={self.node_number: 1}, table=self.table)

    def __radd__(self, other):
        """
        Reverse Add operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        return self.__add__(other)

    def __rsub__(self, other):
        """
        Reverse subtract operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        return -self.__sub__(other)

    def __rmul__(self, other):
        """
        Reverse multiply operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """
        Reverse divide operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        recip_self = self.__pow__(-1.0)
        return recip_self.__mul__(other)

    def __rpow__(self, other):
        """
        Reverse power operation for arithmetic involving Node Objects
        :param other: other element in the operation
        :return: Node representing the result
        """
        return Node(value=other**self.val, partial_derivatives={self.node_number: other**self.val * math.log(other)}, table=self.table)

    def sin(self):
        """
        Sin operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.sin(self.val), partial_derivatives={self.node_number: math.cos(self.val)}, table=self.table)

    def cos(self):
        """
        Cos operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.cos(self.val), partial_derivatives={self.node_number: -math.sin(self.val)}, table=self.table)

    def tan(self):
        """
        Tan operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.tan(self.val), partial_derivatives={self.node_number: 1/math.cos(self.val)**2}, table=self.table)

    def arcsin(self):
        """
        Arcsin operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.asin(self.val), partial_derivatives={self.node_number: 1/(1 - self.val**2)**0.5}, table=self.table)

    def arccos(self):
        """
        Arccos operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.acos(self.val), partial_derivatives={self.node_number: -1/(1 - self.val**2)**0.5}, table=self.table)

    def arctan(self):
        """
        Arctan operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.atan(self.val), partial_derivatives={self.node_number: 1/(1 + self.val**2)}, table=self.table)

    def sinh(self):
        """
        Sinh operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.sinh(self.val), partial_derivatives={self.node_number: math.cosh(self.val)}, table=self.table)

    def cosh(self):
        """
        Cosh operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.cosh(self.val), partial_derivatives={self.node_number: math.sinh(self.val)}, table=self.table)

    def tanh(self):
        """
        Tanh operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.tanh(self.val), partial_derivatives={self.node_number: 1 - math.tanh(self.val)**2}, table=self.table)

    def logistic(self):
        """
        Logistic operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=1 / (1 + math.exp(-self.val)), partial_derivatives={self.node_number: (math.exp(-self.val)) / (1 + math.exp(-self.val))**2}, table=self.table)

    def exp(self):
        """
        Exp operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.exp(self.val), partial_derivatives={self.node_number: math.exp(self.val)}, table=self.table)

    def log(self, base=math.e):
        """
        Log operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=math.log(self.val, base), partial_derivatives={self.node_number: 1/(self.val*math.log(base))}, table=self.table)

    def sqrt(self):
        """
        Sqrt operation for arithmetic involving Node Objects
        :return: Node Object representing the result
        """
        return Node(value=self.val**0.5, partial_derivatives={self.node_number: 1/(2*self.val**0.5)}, table=self.table)