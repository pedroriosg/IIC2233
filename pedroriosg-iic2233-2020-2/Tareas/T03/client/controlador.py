import json
from PyQt5.QtCore import pyqtSignal, QObject
from frontend_sala_espera import SalaEspera, WarningWindow
from frontend_sala_juego import SalaJuego


class Controlador(QObject):

    # Sala de Espera
    mostrar_sala_espera_signal = pyqtSignal()
    crear_label_esperando_signal = pyqtSignal(int)
    actualizar_jugadores_signal = pyqtSignal(list)
    crear_mapa_signal = pyqtSignal(tuple)

    # Sala de Juego
    mostrar_sala_juego_signal = pyqtSignal()
    crear_labels_personal_signal = pyqtSignal(dict)
    crear_labels_otros_signal = pyqtSignal(list)
    crear_labels_chozas_caminos_signal = pyqtSignal(tuple)
    actualizar_labels_personal_signal = pyqtSignal(dict)
    actualizar_labels_otros_signal = pyqtSignal(list)
    actualizar_dados_signal = pyqtSignal(list)
    actualizar_choza_signal = pyqtSignal(tuple)
    warning_signal = pyqtSignal(bool)
    actualizar_camino_signal = pyqtSignal(tuple)
    manejar_carta_signal = pyqtSignal(str)
    nombres_intercambio_signal = pyqtSignal(list)
    solicitud_intercambio_signal = pyqtSignal(dict)
    intercambio_no_apto_signal = pyqtSignal()
    intercambio_final_signal = pyqtSignal(str)
    nombres_fin_partida_signal = pyqtSignal(str)
    resultados_partida_signal = pyqtSignal(list)
    actualizar_label_carretera_signal = pyqtSignal(list)
    empate_carretera_signal = pyqtSignal()

    # Turnos
    cambiar_turno_signal = pyqtSignal(tuple)
    mi_turno_signal = pyqtSignal()

    # Warning Box
    warning_box_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Leemos parametros
        self.leer_parametros_json()

        # Ventanas instanciadas
        self.sala_espera = SalaEspera()
        self.message_box = WarningWindow()
        self.sala_juego = SalaJuego()

        # Conectar señales
        # Sala de Espera
        self.mostrar_sala_espera_signal.connect(self.mostrar_sala_espera)
        self.crear_label_esperando_signal.connect(self.sala_espera.labels_segun_cantidad)
        self.actualizar_jugadores_signal.connect(self.sala_espera.actualizar_jugadores)

        # Sala de Juego
        self.mostrar_sala_juego_signal.connect(self.mostrar_sala_juego)
        self.crear_mapa_signal.connect(self.sala_juego.crear_hexagonos)
        self.crear_labels_personal_signal.connect(self.sala_juego.crear_labels_personal)
        self.crear_labels_otros_signal.connect(self.sala_juego.crear_labels_otros)
        self.crear_labels_chozas_caminos_signal.connect(self.sala_juego.crear_labels_chozas_caminos)
        self.sala_juego.lanzar_dado_signal.connect(self.parent.enviar)
        self.actualizar_labels_personal_signal.connect(self.sala_juego.actualizar_labels_personal)
        self.actualizar_labels_otros_signal.connect(self.sala_juego.actualizar_labels_otros)
        self.actualizar_dados_signal.connect(self.sala_juego.actualizar_dados)
        self.sala_juego.pasar_turno_signal.connect(self.parent.enviar)
        self.sala_juego.verificar_construccion_choza_signal.connect(self.parent.enviar)
        self.actualizar_choza_signal.connect(self.sala_juego.actualizar_choza)
        self.warning_signal.connect(self.sala_juego.warning)
        self.sala_juego.verificar_construccion_camino_signal.connect(self.parent.enviar)
        self.actualizar_camino_signal.connect(self.sala_juego.actualizar_camino)
        self.sala_juego.comprar_signal.connect(self.parent.enviar)
        self.manejar_carta_signal.connect(self.sala_juego.manejar_carta)
        self.sala_juego.enviar_monopolio_signal.connect(self.parent.enviar)
        self.nombres_intercambio_signal.connect(self.sala_juego.setear_nombres_intercmabio)
        self.sala_juego.enviar_intercambio_signal.connect(self.parent.enviar)
        self.solicitud_intercambio_signal.connect(self.sala_juego.solicitud_de_intercambio)
        self.sala_juego.resultado_solicitud_signal.connect(self.parent.enviar)
        self.intercambio_no_apto_signal.connect(self.sala_juego.intercambio_no_apto)
        self.intercambio_final_signal.connect(self.sala_juego.intercambio_final)
        self.nombres_fin_partida_signal.connect(self.sala_juego.nombres_fin_partida)
        self.resultados_partida_signal.connect(self.sala_juego.resultados_partida)
        self.actualizar_label_carretera_signal.connect(self.sala_juego.actualizar_label_carretera)
        self.empate_carretera_signal.connect(self.sala_juego.empate_carretera)

        # Turnos
        self.cambiar_turno_signal.connect(self.sala_juego.cambiar_turno)
        self.mi_turno_signal.connect(self.sala_juego.mi_turno)

        # Señal de WarningBox
        self.warning_box_signal.connect(self.mostrar_warning_window)

    def mostrar_sala_espera(self):
        self.sala_espera.show()

    def mostrar_sala_juego(self):
        self.sala_espera.close()
        self.sala_juego.show()

    def mostrar_warning_window(self):
        self.message_box.show()

    def manejar_mensaje(self, mensaje):

        try:
            comando = mensaje["comando"]
        except KeyError:
            return []

        if comando == "actualizar_jugadores":
            self.actualizar_jugadores_signal.emit(mensaje["nombres_jugadores"])
            self.mostrar_sala_espera_signal.emit()
        elif comando == "armar_sala":
            self.crear_label_esperando_signal.emit(mensaje["numero_jugadores"])
        elif comando == "labels_propios_juego":
            self.crear_labels_personal_signal.emit(mensaje["info"])
        elif comando == "espacio_no_disponible":
            self.warning_box_signal.emit()
        elif comando == "comenzar_partida":
            self.crear_mapa_signal.emit((mensaje["hexagonos"], mensaje["pos_nodos"]))
            self.parent.log("Usuario", "Mapa Creado", "-")
            self.mostrar_sala_juego_signal.emit()
        elif comando == "labels_otros_juego":
            self.crear_labels_otros_signal.emit(mensaje["info"])
        elif comando == "crear_labels_choza_camino":
            tupla = (mensaje["chozas"], mensaje["caminos"])
            self.crear_labels_chozas_caminos_signal.emit(tupla)
        elif comando == "cambiar_turno":
            tupla = (mensaje["nombre_jugador"], mensaje["color"])
            self.cambiar_turno_signal.emit(tupla)
        elif comando == "mi_turno":
            self.mi_turno_signal.emit()
        elif comando == "dps_lanzar":
            self.actualizar_dados_signal.emit(mensaje["dados"])
        elif comando == "actualizar_todo":
            self.actualizar_labels_personal_signal.emit(mensaje["info_personal"])
            self.actualizar_labels_otros_signal.emit(mensaje["info_grupal"])
        elif comando == "choza_verificada":
            tupla = (mensaje["resultado"], mensaje["identificacion"])
            self.actualizar_choza_signal.emit(tupla)
        elif comando == "warning":
            self.warning_signal.emit(mensaje["resultado"])
        elif comando == "camino_verificado":
            tupla = (mensaje["resultado"], mensaje["identificacion"])
            self.actualizar_camino_signal.emit(tupla)
        elif comando == "venta_carta":
            self.manejar_carta_signal.emit(mensaje["tipo_carta"])
        elif comando == "dps_monopolio":
            pass
        elif comando == "nombres_intercambio":
            self.nombres_intercambio_signal.emit(mensaje["info"])
        elif comando == "aceptar_intercambio":
            self.solicitud_intercambio_signal.emit(mensaje)
        elif comando == "intercambio_no_apto":
            self.intercambio_no_apto_signal.emit()
        elif comando == "intercambio_final":
            self.intercambio_final_signal.emit(mensaje["resultado"])
        elif comando == "nombre_fin":
            self.nombres_fin_partida_signal.emit(mensaje["info"])
        elif comando == "resultados":
            self.resultados_partida_signal.emit(mensaje["info"])
        elif comando == "carretera":
            self.actualizar_label_carretera_signal.emit(mensaje["info"])
        elif comando == "empate_carretera":
            self.empate_carretera_signal.emit()

    def leer_parametros_json(self):
        # Acá leemos el archivo JSON
        with open("parametros.json", "rb") as file:
            self.parametros = json.load(file)
            self.asignar_parametros(self.parametros)

    def asignar_parametros(self, parametros):
        self.host = self.parametros["HOST"]
        self.port = self.parametros["PORT"]
