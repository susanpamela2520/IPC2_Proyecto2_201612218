import re

from TDA.Matriz import Matriz


class Convertidor:
    def __init__(self):
        self._matriz = Matriz()

    def llenarMatriz(self, lineas, componentes):
        # for item in elaboracion:
        linea = lineas.obtenerInicio()
        componente = componentes.obtenerInicio()
        # lineas.graficar()
        while linea is not None:
            x = linea.valor.replace("L", "")
            x = int(x.replace("p", "")) - 1
            y = componente.valor.replace("C", "")
            y = int(y.replace("p", "")) - 1
            print('movimiento ', str(linea.valor), str(componente.valor))
            ultimo_componente = self._buscarUltimoComponente(x, y)
            direccion = 1
            if ultimo_componente > 0 and  y < ultimo_componente:
                direccion = -1              #Ve la posicion de los componentes para ir adelante o atras en la linea de ensambleje 

            inicio = self._buscarPosicionDeLinea(x, y)
            if direccion == 1:
                limite_superior = inicio + y + 1 - ultimo_componente
            elif direccion == -1:
                limite_superior = ultimo_componente - y + inicio - 1

            # Donde esta ahorita? como saber cual fue el ultimo componente visitado? en que lugar esta cada linea?
            i = inicio
            while i < limite_superior: #determina la cantidad de posiciones que se mueve el brazo
                #     check if move can be made. Hay ensamble en este fila?
                print("buscando ",x, i)
                temp = self._matriz.obtener(0, i)
                # temp = nodo.abajo
                esta_ensamblando = False
                while temp is not None:
                    if 'Ensamblando' in temp.valor:         #Se recorre horizontalmente si hay un emsambleje o no
                        esta_ensamblando = True
                        break
                    temp = temp.siguiente

                if esta_ensamblando is True:
                    #     si si hay ensamble dejar como no hacer nada
                    self._matriz.insertar(x, i, 'No hacer nada')
                else:
                    #     si no hay ensamble proceder al siguiente movimiento
                    componente_int = self._buscarUltimoComponente(x, i) + direccion
                    if self._matriz.obtener(x, i) is None:
                        self._matriz.insertar(x, i, 'Mover brazo – componente ' + str(componente_int))
                    else:
                        limite_superior += 1   #se incrementa el limite superior para verficar que no haya nada y utilizar el siguiente

                i += 1
            linea = linea.siguiente     
            componente = componente.siguiente #Linea siguiente para trabajar

            self._buscarLugarParaEnsamblar(x, y)

        print("**************************")
        self._matriz.imprimir()
        return self._matriz

    def _buscarLugarParaEnsamblar(self,x, y):
        i = y
        while True:
            # verificar si se puede ensamblar
            temp = self._matriz.obtener(0, i)
            # temp = nodo.abajo
            esta_vacio = True
            while temp is not None:
                if 'No hacer nada' != temp.valor:
                    esta_vacio = False
                    break
                temp = temp.siguiente

            if esta_vacio and self._matriz.obtener(x, i) is None:
                self._matriz.insertar(x, i, 'Ensamblar componente ' + str(y + 1))
                temp = self._matriz.obtener(0, i)
                if temp is None:
                    self._matriz.insertar(0, i, 'No hacer nada')

                temp = self._matriz.obtener(0, i)
                j = 0
                while temp is not None:
                    if j != x:
                        self._matriz.insertar(j, i, 'No hacer nada')
                    j += 1
                    temp = temp.siguiente
                break
            else:
                self._matriz.insertar(x, i, 'No hacer nada')

            i += 1

        self._matriz.imprimir()

    def _buscarUltimoComponente(self, x, y):  #Recorre verticalmente para saber cual es el sigueinte que toca
        i = 0
        temp = self._matriz.obtener(x, i)
        if temp is None:
            return i

        filtro_componentes = re.compile(r'\d+')
        ultimo_componente = None
        while temp is not None:
            if 'componente' in temp.valor:
                ultimo_componente = filtro_componentes.findall(temp.valor)
            temp = temp.siguiente

        if ultimo_componente is not None:
            return int(ultimo_componente[0])

        return 0


    def _buscarPosicionDeLinea(self, x, y):
        i = 0
        temp = self._matriz.obtener(x, i)
        if temp is None:
            return i

        while temp is not None:

            temp = self._matriz.obtener(x, i)
            if temp is not None:
                i += 1

        return i
