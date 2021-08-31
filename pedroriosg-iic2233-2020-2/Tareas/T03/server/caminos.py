class Camino():

    def __init__(self, nodos):
        self.nodos_que_conecta = nodos
        # Estado True si está disponible
        self._id = nodos[0] + nodos[1]
        self.estado = True
        self.usuario = None
        self.color = None
        self.orientacion = None
        self.definir_orientacion()

    def ocupar_camino(self, jugador):
        self.estado = False
        self.usuario = jugador
        self.color = jugador.color

    def definir_orientacion(self):
        nodo_a = self.nodos_que_conecta[0]
        nodo_b = self.nodos_que_conecta[1]
        self.suma_nodos = nodo_a + nodo_b
        if int(nodo_b) - int(nodo_a) == 1:
            self.orientacion = "0"
        elif "4" in nodo_b or "6" in nodo_b or "8" in nodo_b \
             or "0" in nodo_b or ("2" in nodo_b and nodo_b[1] == "2"):
            self.orientacion = "60"
        else:
            self.orientacion = "120"
