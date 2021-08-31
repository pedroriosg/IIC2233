import json
from nodo import Nodo
from caminos import Camino
from hexagono import Hexagono
from generador_grilla import GeneradorGrillaHexagonal
from random import choice


class Mapa():

    def __init__(self, parent, log_activo=True):
        self.parent = parent
        # Preparar Mapa
        self.log_activo = log_activo
        self.dimensiones = None
        self.nodos = []
        self.caminos = []
        self.hexagonos = []
        self.posicion_nodos = None
        self.leer_parametros_json()

    def log(self, cliente, evento, detalle):
        if self.log_activo:
            print(f"{cliente:20s}|{evento:30s}|{detalle: >s}")

    def instanciar_nodos(self):
        for _id in self.info_nodos:
            nodo = Nodo(_id)
            nodo.nodos_adyacentes = self.info_nodos[_id]
            self.nodos.append(nodo)
            self.instanciar_caminos(_id, self.info_nodos[_id])
        self.nodos_dict = {nodo._id: nodo for nodo in self.nodos}
        self.log("Servidor", "Nodos Instanciados", f"Cantidad: {len(self.nodos)}")
        self.log("Servidor", "Caminos Instanciados", f"Cantidad: {len(self.caminos)}")
        self.instanciar_hexagonos()
        self.log("Servidor", "Hexágonos Instanciados", f"Cantidad: {len(self.hexagonos)}")
        self.log("Servidor", "Grilla Generada", "-")

    def instanciar_caminos(self, nodo_inicial, nodos_adyacentes):
        for adyacente in nodos_adyacentes:
            conecta = [int(nodo_inicial), int(adyacente)]
            conecta.sort()
            conexion = [str(conecta[0]), str(conecta[1])]
            if not self.caminos:
                arista = Camino(conexion)
                self.caminos.append(arista)
                continue
            existe = False
            for camino in self.caminos:
                if camino.nodos_que_conecta == conexion:
                    existe = True
            if not existe:
                arista = Camino(conexion)
                self.caminos.append(arista)

    def instanciar_hexagonos(self):
        # Creamos numero de fichas
        ficha_menor = self.parent.parametros["FICHA_MENOR"]
        ficha_mayor = self.parent.parametros["FICHA_MAYOR"]
        exepcion = self.parent.parametros["FICHA_EXEPCION"]
        numero_hexagonos = [str(i) for i in range(0, 10)]
        hexagonos_arcilla = []
        hexagonos_madera = []
        hexagonos_trigo = []
        lista_materias = [hexagonos_arcilla, hexagonos_madera, hexagonos_trigo]
        for _ in range(3):
            hex_arcilla = choice(numero_hexagonos)
            hexagonos_arcilla.append(hex_arcilla)
            numero_hexagonos.remove(hex_arcilla)
            hex_madera = choice(numero_hexagonos)
            hexagonos_madera.append(hex_madera)
            numero_hexagonos.remove(hex_madera)
            hex_trigo = choice(numero_hexagonos)
            hexagonos_trigo.append(hex_trigo)
            numero_hexagonos.remove(hex_trigo)
        for _ in range(1):
            hex_incognito = choice(numero_hexagonos)
            lista_incognita = choice(lista_materias)
            lista_incognita.append(hex_incognito)
            numero_hexagonos.remove(hex_incognito)

        numero_fichas = [numero for numero in range(ficha_menor, ficha_mayor + 1)
                         if numero != exepcion]
        materias_primas = {"arcilla": hexagonos_arcilla, "madera": hexagonos_madera,
                           "trigo": hexagonos_trigo}
        for _id in self.info_hexagonos:
            for materia in materias_primas:
                if _id in materias_primas[materia]:
                    recurso = materia
            adyacentes = self.info_hexagonos[_id]
            numero = choice(numero_fichas)
            numero_fichas.remove(numero)
            hexagono = Hexagono(_id, adyacentes, numero, recurso)
            self.hexagonos.append(hexagono)
        self.asignar_materias_primas_a_nodo()
        self.generar_grilla()

    def asignar_materias_primas_a_nodo(self):
        # Asignamos la materia prima a cada nodo perteneciente al hexágono
        for hexagono in self.hexagonos:
            for nodos in hexagono.nodos:
                nodo = self.nodos_dict[nodos]
                nodo.asignar_materia_prima(hexagono.materia_prima)
        self.log("Servidor", "Asignando Materias a Nodos", "-")

    def leer_parametros_json(self):
        # Acá leemos el archivo JSON
        with open("grafo.json", "rb") as file:
            informacion = json.load(file)
            self.asignar_parametros(informacion)

    def asignar_parametros(self, informacion):
        self.dimensiones = informacion["dimensiones_mapa"]
        self.info_nodos = informacion["nodos"]
        self.info_hexagonos = informacion["hexagonos"]
        self.instanciar_nodos()

    def generar_grilla(self):
        pixeles = self.parent.parametros["PIXELES_HEXAGONO"]
        pos_x = self.parent.parametros["POS_X_GRILLA"]
        pos_y = self.parent.parametros["POS_Y_GRILLA"]
        grilla = GeneradorGrillaHexagonal(pixeles)
        self.posicion_nodos = grilla.generar_grilla(self.dimensiones, pos_x, pos_y)

    def envio_hexagonos(self):
        self.log("Servidor", "Envío de Hexágonos", "Informacion")
        return {h._id: [h.numero, h.materia_prima] for h in self.hexagonos}

    def envio_nodos(self):
        self.log("Servidor", "Envío de Chozas", "Informacion")
        return {nodo._id: nodo.color for nodo in self.nodos_dict.values()}

    def envio_caminos(self):
        self.log("Servidor", "Envío de Caminos", "Informacion")
        return {camino.suma_nodos: [camino.color, camino.orientacion] for camino in self.caminos}


if __name__ == "__main__":
    mapa = Mapa()
