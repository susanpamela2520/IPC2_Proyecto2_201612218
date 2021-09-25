import xml.dom.minidom

from reportlab.platypus.paragraph import strip

from TDA.Cola import Cola
from TDA.Diccionario import Diccionario


class Lector:
    TYPE_MAQUINA = "maquina"
    TYPE_SIMULACION = "simulacion"

    def __init__(self, ruta, type):
        self.type = type
        self.ruta = ruta

    def leer(self):
        if self.type == self.TYPE_MAQUINA:
            return self._parsearMaquina(self.ruta)
        elif self.type == self.TYPE_SIMULACION:
            return self._parsearSimulacion(self.ruta)

    def _parsearMaquina(self, ruta):
        # use the parse() function to load and parse an XML file
        data = Diccionario()
        doc = xml.dom.minidom.parse(ruta)

        root = doc.getElementsByTagName("Maquina")[0]

        cantidadLineasProduccion = root.getElementsByTagName("CantidadLineasProduccion")
        data.insertar('cantidad_lineas_produccion', int(strip(cantidadLineasProduccion[0].firstChild.nodeValue)))
        # print(cantidadLineasProduccion[0].firstChild.nodeValue)

        listadoLineasProduccion = root.getElementsByTagName("ListadoLineasProduccion")[0]
        lineasProduccion = listadoLineasProduccion.getElementsByTagName("LineaProduccion")

        lineas = Cola()
        for linea in lineasProduccion:
            linea_produccion = Diccionario()
            numero = linea.getElementsByTagName("Numero")
            linea_produccion.insertar('numero', int(strip(numero[0].firstChild.nodeValue)))

            componentes = linea.getElementsByTagName("CantidadComponentes")
            linea_produccion.insertar('componentes', int(strip(componentes[0].firstChild.nodeValue)))

            tiempo = linea.getElementsByTagName("TiempoEnsamblaje")
            linea_produccion.insertar('tiempo', int(strip(tiempo[0].firstChild.nodeValue)))
            lineas.push(linea_produccion)

        data.insertar('lineas_produccion', lineas)

        listadoProductos = root.getElementsByTagName("ListadoProductos")[0]
        productos = listadoProductos.getElementsByTagName("Producto")

        list_productos = Cola()

        for producto in productos:
            product = Diccionario()
            nombre = producto.getElementsByTagName("nombre")
            product.insertar('nombre', strip(nombre[0].firstChild.nodeValue))

            elaboracion = producto.getElementsByTagName("elaboracion")
            elaboracion_str = strip(elaboracion[0].firstChild.nodeValue)
            # elaboracion_arr = elaboracion_str.split(" ")
            product.insertar('elaboracion', elaboracion_str)
            list_productos.push(product)

        data.insertar('products', list_productos)
        return data

    def _parsearSimulacion(self, ruta):
        pass
