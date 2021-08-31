class Nodo:

    def __init__(self, _id):
        self._id = _id
        # Estado True es que está libre
        self.estado = True
        self.usuario = None
        self.nodos_adyacentes = None
        self.materias_primas = []
        self.color = None

    def ocupar_nodo(self, jugador):
        self.estado = False
        self.usuario = jugador
        self.color = jugador.color

    def asignar_materia_prima(self, materia):
        self.materias_primas.append(materia)
