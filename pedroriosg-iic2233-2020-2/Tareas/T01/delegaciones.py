import parametros as p
from abc import ABC, abstractmethod
from random import uniform


class Delegaciones(ABC):

    def __init__(self, nombre, entrenador, equipo, medallas, moral, dinero):
        self.nombre = nombre
        self.entrenador = entrenador
        self.equipo = equipo
        self.medallas = medallas
        self.__moral = moral
        self.dinero = dinero
        self.exelencia_y_respeto = 0  # At distinto para cada delegación
        self.implementos_deportivos = 0  # At distinto para cada delegación
        self.implementos_medicos = 0  # At distinto para cada delegación

    @property
    def moral(self):
        return self.__moral

    @moral.setter
    def moral(self, value):
        if value > p.MAX_MORAL_DELEGACIONES:
            self.__moral = p.MAX_MORAL_DELEGACIONES
        elif value < p.MIN_MORAL_DELEGACIONES:
            self.__moral = p.MIN_MORAL_DELEGACIONES
        else:
            self.__moral = value

    def fichar_deportistas(self, diccionario):
        print("\nA continuación, se muestran los deportistas que puedes fichar:\n")
        # A continuacion, mostramos datos
        # Variables NO descriptivas para acortar lineas
        print(f"NOMBRE DEPORTISTA{15 * ' '}VELOCIDAD   RESISTENCIA"
              "  FLEXIBILIDAD   MORAL   PRECIO   LESION\n")
        for d in diccionario.values():
            lista = [(d.nombre, d.velocidad, d.resistencia, d.flexibilidad,
                      d.lesionado, d.moral, d._precio)]
            for n, v, r, f, l, m, pr in lista:
                print(f"{n:35s}{v: <3.0f}{11 * ' '}{r: <3.0f}{11 * ' '}{f: <3.0f}"
                      f"{8 * ' '}{m: <3.0f}{5 * ' '}{pr: <3.0f}{5 * ' '}{str(l):>s}")
        # Aca seleccionamos el deportista a fichar
        t = True
        while t:  # Comienza el ciclo para seleccionar
            nombre = input("\nSelecciona el nombre del deportista a fichar: ")
            if nombre in diccionario:  # Vemos si el jugador existe
                t = False
                if diccionario[nombre]._precio > self.dinero:  # Vemos si hay dinero para comprar
                    print("\nNo es posible fichar a este deportista. Dinero bajo.")
                else:
                    self.equipo.append(diccionario[nombre])  # Fichaje valido
                    print(f"\nFichaste a {nombre}!")
                    self.dinero -= diccionario[nombre]._precio
                    del diccionario[nombre]
            else:  # Si el jugador no existe
                print("\nEste jugador no existe!\nIngresa el nombre exacto!")

    def entrenar_deportistas(self):
        print("\nA continuación, se muestran los deportistas que puedes entrenar:\n")
        # A continuacion, mostramos datos
        # Variables NO descriptivas para acortar lineas
        print(f"NUMER0  NOMBRE DEPORTISTA{15 * ' '}VELOCIDAD   RESISTENCIA"
              "  FLEXIBILIDAD\n")
        c = 0  # Contador para el print
        lista_numeros = []
        for d in self.equipo:
            datos = [(d.nombre, d.velocidad, d.resistencia, d.flexibilidad)]
            for n, v, r, f in datos:
                print(f"{c}{7 * ' '}{n:35s}{v: <3.0f}{11 * ' '}{r: <3.0f}{11 * ' '}{f: <3.0f}")
                lista_numeros.append(str(c))
                c += 1
        # Aca seleccionamos el deportista a entrenar
        k = True
        while k:  # Comienza el ciclo para seleccionar
            numero = input("\nSelecciona el número del deportista a entrenar: ")
            if numero in lista_numeros:  # Vemos si existe el deportista seleccionado
                t = True
                k = False
                opciones = ["0", "1", "2"]
                # Mostramos atributos a entrenar
                while t:  # Ciclo para seleccionar atributo
                    print("\nSeleccione atributo a mejorar:\n")
                    print("[0] Velocidad")
                    print("[1] Resistencia")
                    print("[2] Flexibilidad\n")
                    # Seleccionamos el atributo a entrenar
                    atributo = input("Seleccione atributo: ")
                    if atributo in opciones:
                        t = False
                        self.dinero -= p.COSTO_ENTRENAR_DEPORTISTA
                        if self.nombre == "IEEEsparta":
                            # Si es de IEEEsparta, entrenamiento efectivo
                            self.equipo[int(numero)].entrenar(atributo,
                                                              p.EFECTIVIDAD_ENTRENAMIENTO_IEEE)
                        else:
                            # Si es DCCrotona, entrenamiento normal
                            self.equipo[int(numero)].entrenar(atributo,
                                                              p.EFECTIVIDAD_ENTRENAMIENTO_DCC)
                    else:  # Si el atributo no existe
                        print("\nOpción inválida. Ingrese nuevamente.")
            else:  # Si el jugador no existe
                print("\nOpción inválida. Ingrese nuevamente.")

    def sanar_lesiones(self, delegacion):
        # Aca se muestran los nombres de deportistas lesionados
        # Solo muestro nombres, ya que el atributo lesion es TRUE
        print("\nA continuación, se muestran los deportistas que puedes sanar:\n")
        lista_numeros = []
        for indice in range(0, len(self.equipo)):
            if self.equipo[indice].lesionado:
                print(f"[{indice}] {self.equipo[indice].nombre}")
                lista_numeros.append(str(indice))
        t = True
        # Chequeo que existan lesionados
        if len(lista_numeros) == 0:
            print("Todos los deportistas están sanos.")
            t = False
        while t:
            # Selecciono numero de deportista a sanar
            numero = input("\nSelecciona el número del deportista a sanar: ")
            if numero in lista_numeros:  # Veo si existe el numero del deportista
                t = False
                if delegacion.nombre == "DCCrotona":
                    self.dinero -= (p.COSTO_SANAR_DEPORTISTA * 2)  # La delegacion DCCrotona paga el doble sanar
                else:
                    self.dinero -= (p.COSTO_SANAR_DEPORTISTA)  # La delegacion IEEEsparta paga normal
                deportista = self.equipo[int(numero)]
                # Aca calculamos probabilidad de sanar lesion segun enunciado
                probabilidad = min(p.INFERIOR_MIN, max(p.INFERIOR_MAX, (deportista.moral *
                                                       (self.implementos_medicos +
                                                       self.exelencia_y_respeto)) / p.DIVISOR))
                probabilidad = round(probabilidad, 1)
                # Creamos numero aleatorio
                numero_aleatorio = uniform(0, 1)
                numero_aleatorio = round(numero_aleatorio, 1)
                if numero_aleatorio <= probabilidad:  # Comparamos para ver si se sana
                    deportista.lesionado = False
                else:
                    print("\nDeportista NO sanado.")
            else:
                print("\nOpción inválida. Ingrese nuevamente")

    def comprar_tecnologia(self):
        self.dinero -= p.COSTO_TECNOLOGIA  # Restamos precio tecnologia
        print("\nMEJORANDO IMPLEMENTOS...")
        # Aumentamos ambos implementos de la delegacion
        self.implementos_deportivos = self.implementos_deportivos * \
            p.AUMENTO_EFECTIVIDAD_IMPLEMENTOS
        self.implementos_medicos = self.implementos_deportivos * \
            p.AUMENTO_EFECTIVIDAD_IMPLEMENTOS
        print(F"Implementos deportivos: {self.implementos_deportivos}")
        print(F"Implementos medicos: {self.implementos_medicos}")

    @abstractmethod
    def habilidad_especial(self):
        pass


class IEEEsparta(Delegaciones):

    def __init__(self, nombre, entrenador, equipo, medallas, moral, dinero):
        super().__init__(nombre, entrenador, equipo, medallas, moral, dinero)
        self.exelencia_y_respeto = uniform(p.MIN_EXELECIA_RESPETO_IEE,
                                           p.MAX_EXELECIA_RESPETO_IEE)
        self.implementos_deportivos = uniform(p.MIN_IMP_DEPORTIVOS_IEE,
                                              p.MAX_IMP_DEPORTIVOS_IEE)
        self.implementos_medicos = uniform(p.MIN_IMP_MEDICOS_IEE,
                                           p.MAX_IMP_MEDICOS_IEE)

    def habilidad_especial(self):
        print("\nUTILIZANDO HABILIDAD ESPECIAL")
        print("ARRRGG!!! SUBIENDO MORAL AL MÁXIMO")
        # Aumentamos la moral de cada deportista a 100
        for deportista in self.equipo:
            deportista.moral = p.MAX_MORAL_DEPORTISTAS
        self.dinero -= p.COSTO_HABILIDAD_ESPECIAL  # Costo de habilidad especial


class DCCrotona(Delegaciones):

    def __init__(self, nombre, entrenador, equipo, medallas, moral, dinero):
        super().__init__(nombre, entrenador, equipo, medallas, moral, dinero)
        self.exelencia_y_respeto = uniform(p.MIN_EXELECIA_RESPETO_DCC,
                                           p.MAX_EXELECIA_RESPETO_DCC)
        self.implementos_deportivos = uniform(p.MIN_IMP_DEPORTIVOS_DCC,
                                              p.MAX_IMP_DEPORTIVOS_DCC)
        self.implementos_medicos = uniform(p.MIN_IMP_MEDICOS_DCC,
                                           p.MAX_IMP_MEDICOS_DCC)

    def habilidad_especial(self):
        print("\nUTILIZANDO HABILIDAD ESPECIAL")
        print("GANANDO MEDALLAS Y DINERO")
        self.medallas += 1
        self.exelencia_y_respeto += p.PREMIO_EXE_RESP_GANADOR
        self.dinero += p.DINERO_GANADOR
        self.dinero -= p.COSTO_HABILIDAD_ESPECIAL  # Costo de habilidad especial
