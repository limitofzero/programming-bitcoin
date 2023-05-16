from point import Point
from ecc import FieldElement

prime = 223
a = FieldElement(0, prime)
b = FieldElement(7, prime)
x1 = FieldElement(15, prime)
y1 = FieldElement(86, prime)

start_point = Point(x1, y1, a, b)
infinity = Point(None, None, a, b)

p = start_point
order = 1
while p != infinity:
    order += 1
    p += start_point

print(order)
