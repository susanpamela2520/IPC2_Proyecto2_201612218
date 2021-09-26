import xml.dom.minidom

from reportlab.platypus.paragraph import strip

from TDA.Cola import Cola
from TDA.Diccionario import Diccionario


class Lector:
    TYPE_MAQUINA = "maquina"
    TYPE_SIMULACION = "simulacion"

    def __init__(self, ruta, type):   #Recibe ruta y tipo
        self.type = type
        self.ruta = ruta

    def leer(self):                    #Lee archivo y Retorna objeto diccionario 
        if self.type == self.TYPE_MAQUINA:
            return self._parsearMaquina(self.ruta)
        elif self.type == self.TYPE_SIMULACION:
            return self._parsearSimulacion(self.ruta)

    def _parsearMaquina(self, ruta):   #Lee archivo tipo maquina para poder navergar en el diccionario
        # use the parse() function to load and parse an XML file
        data = Diccionario()
        doc = xml.dom.minidom.parse(ruta)

        root = doc.getElementsByTagName("Maquina")[0]  #Lecturas de palabras claves

        cantidadLineasProduccion = root.getElementsByTagName("CantidadLineasProduccion")
        data.insertar('cantidad_lineas_produccion', int(strip(cantidadLineasProduccion[0].firstChild.nodeValue)))
        # print(cantidadLineasProduccion[0].firstChild.nodeValue)

        listadoLineasProduccion = root.getElementsByTagName("ListadoLineasProduccion")[0]
        lineasProduccion = listadoLineasProduccion.getElementsByTagName("LineaProduccion")

        lineas = Cola()   #Creacion de cola para la lectura de archivo
        for linea in lineasProduccion:
            linea_produccion = Diccionario() #Para obtener los datos del archivo se va recorriendo con el for
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

        list_productos = Cola()  #Se repite la misma historia jajaja

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

            #inserta el nodo como valor para luego recorrero 
            
    def _parsearSimulacion(self, ruta):
        pass
