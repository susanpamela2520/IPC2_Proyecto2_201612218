from TDA.Cola import Cola
from TDA.Pila import Pila

cola = Pila()
print(cola.estaVacia())
cola.push(1)
cola.push(2)
print(cola.estaVacia())
cola.push(3)
print(cola.size())
print(cola.pop())
print(cola.pop())
print(cola.estaVacia())
print(cola.pop())
print(cola.estaVacia())