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
                       num_inputs=len(self.der))
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
                       num_inputs=len(self.der))
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
            return Row(value=self.val * other.val, derivative=current_derivative, num_inputs=len(self.der))
        except AttributeError:
            current_derivative = [other * der for der in self.der]
            return Row(value=self.val * other, derivative=current_derivative, num_inputs=len(self.der))

    def __truediv__(self, other):
        """
        Division operation for arithmetic involving Row Objects.
        :param other: The other element in the division operation.
        :return: Row Object representing the quotient
        """
        try:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative.append((other.val * self.der[i] - self.val * other.der[i]) / (np.square(other.val)))
            return Row(value=self.val / other.val, derivative=current_derivative, num_inputs=len(self.der))
        except AttributeError:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative = [der / other for der in self.der]
            return Row(value=self.val / other, derivative=current_derivative, num_inputs=len(self.der))

    def __pow__(self, other):
        """
        Power operation for arithmetic involving Row Objects
        :param other: The other element in the power operation.
        :return: Row Object representing the result
        """
        try:
            current_derivative = list()
            for i in range(len(self.der)):
                current_derivative.append(
                    self.val ** other.val * (other.der[i] * np.log(self.val) + other.val * self.der[i] / self.val))
            return Row(value=self.val ** other.val, derivative=current_derivative, num_inputs=len(self.der))
        except AttributeError:
            current_derivative = [other * self.val ** (other - 1) * der for der in self.der]
            return Row(value=self.val ** other, derivative=current_derivative, num_inputs=len(self.der))

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
            current_derivative.append(other ** self.val * (math.log(other)) * self.der[i])
        return Row(value=other ** self.val, derivative=current_derivative, num_inputs=len(self.der))

    def __eq__(self, other):
        try:
            return self.val == other.val and self.der == other.der
        except AttributeError:
            return self.val == other

    def __ne__(self, other):
        try:
            return self.val != other.val or self.der != other.der
        except AttributeError:
            return self.val != other

    def sin(self):
        """
        Sin operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.sin(self.val), derivative=[math.cos(self.val) * der for der in self.der],
                   num_inputs=len(self.der))

    def cos(self):
        """
        Cos operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.cos(self.val), derivative=[-math.sin(self.val) * der for der in self.der],
                   num_inputs=len(self.der))

    def tan(self):
        """
        Tan operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.tan(self.val), derivative=[(1.0 / math.cos(self.val) ** 2) * der for der in self.der],
                   num_inputs=len(self.der))

    def arcsin(self):
        """
        Arcsin operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.asin(self.val), derivative=[(1 / (1 - self.val ** 2) ** 0.5) * der for der in self.der],
                   num_inputs=len(self.der))

    def arccos(self):
        """
        Arccos operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.acos(self.val), derivative=[-(1 / (1 - self.val ** 2) ** 0.5) * der for der in self.der],
                   num_inputs=len(self.der))

    def arctan(self):
        """
        Arctan operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.atan(self.val), derivative=[(1 / (1 + self.val ** 2)) * der for der in self.der],
                   num_inputs=len(self.der))

    def sinh(self):
        """
        Sinh operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.sinh(self.val),
                   derivative=[math.cosh(self.val) * der for der in self.der], num_inputs=len(self.der))

    def cosh(self):
        """
        Cosh operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.cosh(self.val),
                   derivative=[math.sinh(self.val) * der for der in self.der], num_inputs=len(self.der))

    def tanh(self):
        """
        Tanh operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.tanh(self.val),
                   derivative=[1 / (math.cosh(self.val) ** 2) * der for der in self.der], num_inputs=len(self.der))

    def exp(self):
        """
        Exp operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=np.exp(self.val), derivative=[np.exp(self.val) * der for der in self.der],
                   num_inputs=len(self.der))

    def log(self, base=math.e):
        """
        Log operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.log(self.val, base),
                   derivative=[1.0 / (self.val * math.log(base, math.e)) * der for der in self.der],
                   num_inputs=len(self.der))

    def sqrt(self):
        """
        Sqrt operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=math.sqrt(self.val), derivative=[1.0 / (2.0 * self.val ** 0.5) * der for der in self.der],
                   num_inputs=len(self.der))

    def logistic(self):
        """
        Logistic operation for arithmetic involving Row Objects
        :return: Row Object representing the result
        """
        return Row(value=1 / (1 + math.exp(-self.val)),
                   derivative=[(math.exp(-self.val)) / ((math.exp(-self.val) + 1) ** 2) * der for der in self.der],
                   num_inputs=len(self.der))


class RowVector:

    def __init__(self, input, initialization=True):
        if initialization:
            self.rows = list()
            for i in range(len(input)):
                self.rows.append(Row(value=input[i], derivative=[1]))
        else:
            self.rows = input

        self.val = [row.val for row in self.rows]
        self.der = [row.der[0] for row in self.rows]

    def __add__(self, other):
        try:
            return RowVector([row + other for row in self.rows], initialization=False)
        except TypeError:
            current_rows = list()
            for i in range(len(self.rows)):
                current_rows.append(self.rows[i] + other.rows[i])
            return RowVector(current_rows, initialization=False)

    def __sub__(self, other):
        """
        Subtraction operation for arithmetic involving RowVector Objects.
        :param other: The other element in the subtraction operation.
        :return: RowVector Object representing the Difference
        """
        try:
            return RowVector([row - other for row in self.rows], initialization=False)
        except TypeError:
            current_rows = list()
            for i in range(len(self.rows)):
                current_rows.append(self.rows[i] - other.rows[i])
            return RowVector(current_rows, initialization=False)

    def __mul__(self, other):
        """
        Multiplication operation for arithmetic involving RowVector Objects.
        :param other: The other element in the multiplication operation.
        :return: RowVector Object representing product.
        """
        try:
            return RowVector([row * other for row in self.rows], initialization=False)
        except TypeError:
            current_rows = list()
            for i in range(len(self.rows)):
                current_rows.append(self.rows[i] * other.rows[i])
            return RowVector(current_rows, initialization=False)

    def __truediv__(self, other):
        """
        Division operation for arithmetic involving RowVector Objects.
        :param other: The other element in the division operation.
        :return: RowVector Object representing the quotient
        """
        try:
            return RowVector([row / other for row in self.rows], initialization=False)
        except TypeError:
            current_rows = list()
            for i in range(len(self.rows)):
                current_rows.append(self.rows[i] / other.rows[i])
            return RowVector(current_rows, initialization=False)

    def __pow__(self, other):
        """
        Power operation for arithmetic involving RowVector Objects
        :param other: The other element in the power operation.
        :return: RowVector Object representing the result
        """
        try:
            return RowVector([row ** other for row in self.rows], initialization=False)
        except TypeError:
            current_rows = list()
            for i in range(len(self.rows)):
                current_rows.append(self.rows[i] ** other.rows[i])
            return RowVector(current_rows, initialization=False)

    def __neg__(self):
        """
        Neg operation for arithmetic involving RowVector Objects
        :return: RowVector Object Representing the Negation
        """
        return RowVector([-row for row in self.rows], initialization=False)

    def __pos__(self):
        """
        Pos operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the Row
        """
        return RowVector([row for row in self.rows], initialization=False)

    def __radd__(self, other):
        """
        Reverse Addition operation for arithmetic involving RowVector Objects.
        :param other: The other element in the addition operation.
        :return: RowVector Object representing the Sum
        """
        return self.__add__(other)

    def __rsub__(self, other):
        """
        Reverse Subtraction operation for arithmetic involving RowVector Objects.
        :param other: The other element in the subtraction operation.
        :return: RowVector Object representing the Difference
        """
        return -self.__sub__(other)

    def __rmul__(self, other):
        """
        Reverse Multiplication operation for arithmetic involving RowVector Objects.
        :param other: The other element in the multiplication operation.
        :return: RowVector Object representing product.
        """
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """
        Reverse Division operation for arithmetic involving RowVector Objects.
        :param other: The other element in the division operation.
        :return: RowVector Object representing the quotient
        """
        recip_self = self.__pow__(-1.0)
        return recip_self.__mul__(other)

    def __rpow__(self, other):
        """
        Reverse Power operation for arithmetic involving RowVector Objects
        :param other: The other element in the power operation.
        :return: RowVector Object representing the result
        """

        return RowVector([other ** row for row in self.rows], initialization=False)

    def __eq__(self, other):
        try:
            return self.rows == other.rows
        except AttributeError:
            return self.rows == other

    def __ne__(self, other):
        try:
            return self.rows != other.rows
        except AttributeError:
            return self.rows != other

    def sin(self):
        """
        Sin operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.sin() for row in self.rows], initialization=False)

    def cos(self):
        """
        Cos operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.cos() for row in self.rows], initialization=False)

    def tan(self):
        """
        Tan operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.tan() for row in self.rows], initialization=False)

    def arcsin(self):
        """
        Arcsin operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.arcsin() for row in self.rows], initialization=False)

    def arccos(self):
        """
        Arccos operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.arccos() for row in self.rows], initialization=False)

    def arctan(self):
        """
        Arctan operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.arctan() for row in self.rows], initialization=False)

    def sinh(self):
        """
        Sinh operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.sinh() for row in self.rows], initialization=False)

    def cosh(self):
        """
        Cosh operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.cosh() for row in self.rows], initialization=False)

    def tanh(self):
        """
        Tanh operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.tanh() for row in self.rows], initialization=False)

    def exp(self):
        """
        Exp operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.exp() for row in self.rows], initialization=False)

    def log(self, base=math.e):
        """
        Log operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.log(base) for row in self.rows], initialization=False)

    def sqrt(self):
        """
        Sqrt operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.sqrt() for row in self.rows], initialization=False)

    def logistic(self):
        """
        Logistic operation for arithmetic involving RowVector Objects
        :return: RowVector Object representing the result
        """
        return RowVector([row.logistic() for row in self.rows], initialization=False)
