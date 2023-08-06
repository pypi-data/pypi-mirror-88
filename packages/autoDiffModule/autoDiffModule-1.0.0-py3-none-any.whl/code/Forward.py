import numpy as np
import math

"""
Row class holds the value and the derivative of input and intermediate variables in the trace table formed when
performing automatic differentiation. 
"""


class Row:

    def __init__(self, value, num_inputs=1, derivative=[1.0]):
        self.val = value
        if len(derivative) == num_inputs:
            self.der = derivative
        else:
            raise Exception("derivative input does not match number of inputs")

    def __add__(self, other):
        """
        Addition operation for arithmetic involving Row Objects.
        :param other: The other element in the addition operation.
        :return: Row Object representing the Sum
        """
        try:
            return Row(value=self.val + other.val, derivative=[a + b for a, b in zip(self.der, other.der)],
                      num_inputs = len(self.der))
        except AttributeError:
            return Row(value=self.val + other, derivative=self.der, num_inputs=len(self.der))

    def __sub__(self, other):
        """
        Subtraction operation for arithmetic involving Row Objects.
        :param other: The other element in the subtraction operation.
        :return: Row Object representing the Difference
        """
        try:
            return Row(value=self.val - other.val, derivative=[a - b for a, b in zip(self.der, other.der)],
                      num_inputs = len(self.der))
        except AttributeError:
            return Row(value=self.val - other, derivative=self.der, num_inputs=len(self.der))

    def __mul__(self, other):
        """
        Multiplication operation for arithmetic involving Row Objects.
        :param other: The other element in the multiplication operation.
        :return: Row Object representing product.
        """
        try:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative.append(self.val * other.der[i] + self.der[i] * other.val)
            return Row(value=self.val * other.val, derivative = current_derivative, num_inputs = len(self.der))
        except AttributeError:
            current_derivative = [other*der for der in self.der]
            return Row(value=self.val * other, derivative=current_derivative, num_inputs = len(self.der))

    def __truediv__(self, other):
        """
        Division operation for arithmetic involving Row Objects.
        :param other: The other element in the division operation.
        :return: Row Object representing the quotient
        """
        try:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative.append((other.val * self.der[i] - self.val * other.der[i])/(np.square(other.val)))
            return Row(value=self.val/other.val, derivative=current_derivative, num_inputs=len(self.der))
        except AttributeError:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative = [der/other for der in self.der]
            return Row(value=self.val/other, derivative=current_derivative, num_inputs=len(self.der))

    def __pow__(self, other):
        """
        Power operation for arithmetic involving Row Objects
        :param other: The other element in the power operation.
        :return: Row Object representing the result
        """
        try:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative.append(self.val**other.val * (other.der[i] * np.log(self.val) + other.val * self.der[i] / self.val))
            return Row(value=self.val**other.val, derivative=current_derivative, num_inputs=len(self.der))
        except AttributeError:
            current_derivative = [other * self.val**(other - 1) * der for der in self.der]
            return Row(value=self.val**other, derivative=current_derivative, num_inputs=len(self.der))

    def __neg__(self):
        """
        Neg operation for arithmetic involving Row Objects
        :return: Row Object Representing the Negation
        """
        return Row(value=-self.val, derivative=[-der for der in self.der], num_inputs=len(self.der))

    def __pos__(self):
        """
        Pos operation for arithmetic involving Row Objects
        :return: Row Object representing the Row
        """
        return Row(value=self.val, derivative=self.der, num_inputs=len(self.der))

    def __radd__(self, other):
        """
        Reverse Addition operation for arithmetic involving Row Objects.
        :param other: The other element in the addition operation.
        :return: Row Object representing the Sum
        """
        return self.__add__(other)

    def __rsub__(self, other):
        """
        Reverse Subtraction operation for arithmetic involving Row Objects.
        :param other: The other element in the subtraction operation.
        :return: Row Object representing the Difference
        """
        return -self.__sub__(other)

    def __rmul__(self, other):
        """
        Reverse Multiplication operation for arithmetic involving Row Objects.
        :param other: The other element in the multiplication operation.
        :return: Row Object representing product.
        """
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """
        Reverse Division operation for arithmetic involving Row Objects.
        :param other: The other element in the division operation.
        :return: Row Object representing the quotient
        """
        recip_self = self.__pow__(-1.0)
        return recip_self.__mul__(other)

    def __rpow__(self, other):
        """
        Reverse Power operation for arithmetic involving Row Objects
        :param other: The other element in the power operation.
        :return: Row Object representing the result
        """
        current_derivative = list()
        for i in range(len(self.der)):
            current_derivative.append(other**self.val * (math.log(other)) * self.der[i])
        return Row(value=other**self.val, derivative=current_derivative, num_inputs=len(self.der))

    def sin(self):
        """
        Sin operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.sin(self.val), derivative=[math.cos(self.val) * der for der in self.der], num_inputs=len(self.der))

    def cos(self):
        """
        Cos operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.cos(self.val), derivative=[-math.sin(self.val) * der for der in self.der], num_inputs=len(self.der))

    def tan(self):
        """
        Tan operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.tan(self.val), derivative=[(1.0/math.cos(self.val)**2) * der for der in self.der], num_inputs=len(self.der))

    def exp(self):
        """
        Exp operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=np.exp(self.val), derivative=[np.exp(self.val) * der for der in self.der], num_inputs=len(self.der))

    def log(self, base=math.e):
        """
        Log operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.log(self.val, base), derivative=[1.0/(self.val * math.log(base, math.e))* der for der in self.der], num_inputs=len(self.der))

    def sqrt(self):
        """
        Sqrt operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.sqrt(self.val), derivative=[1.0/(2.0*self.val**0.5)* der for der in self.der], num_inputs=len(self.der))
