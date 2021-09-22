import xml.dom.minidom


class Lector:
    TYPE_MAQUINA = "maquina"
    TYPE_SIMULACION = "simulacion"

    def __init__(self, ruta, type):
        if type == self.TYPE_MAQUINA:
            self.parsearMaquina(ruta)
        elif type == self.TYPE_SIMULACION:
            self.parsearSimulacion(ruta)

    def parsearMaquina(self, ruta):
        # use the parse() function to load and parse an XML file
        doc = xml.dom.minidom.parse(ruta)

        root = doc.getElementsByTagName("Maquina")[0]

        cantidadLineasProduccion = root.getElementsByTagName("CantidadLineasProduccion")
        print(cantidadLineasProduccion[0].firstChild.nodeValue)

        listadoLineasProduccion = root.getElementsByTagName("ListadoLineasProduccion")[0]
        lineasProduccion = listadoLineasProduccion.getElementsByTagName("LineaProduccion")
        for linea in lineasProduccion:
            numero = linea.getElementsByTagName("Numero")
            print(numero[0].firstChild.nodeValue)

            componentes = linea.getElementsByTagName("CantidadComponentes")
            print(componentes[0].firstChild.nodeValue)

            tiempo = linea.getElementsByTagName("TiempoEnsamblaje")
            print(tiempo[0].firstChild.nodeValue)

        listadoProductos = root.getElementsByTagName("ListadoProductos")[0]
        productos = listadoProductos.getElementsByTagName("Producto")
        for producto in productos:
            nombre = producto.getElementsByTagName("nombre")
            print(nombre[0].firstChild.nodeValue)

            elaboracion = producto.getElementsByTagName("elaboracion")
            print(elaboracion[0].firstChild.nodeValue)

    def parsearSimulacion(self, ruta):
        pass
