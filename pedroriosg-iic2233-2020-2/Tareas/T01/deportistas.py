import parametros as p
from random import uniform


class Deportistas():

    def __init__(self, nombre, flexibilidad, moral, precio, velocidad,
                 lesionado, resistencia):
        self.nombre = nombre
        self.__flexibilidad = flexibilidad
        self.__moral = moral
        self._precio = precio  # Atributo que no debiera modificarse
        self.__velocidad = velocidad
        self.lesionado = lesionado
        self.__resistencia = resistencia

    @property
    def moral(self):
        return self.__moral

    @moral.setter
    def moral(self, value):
        if value >= p.MAX_MORAL_DEPORTISTAS:
            self.__moral = p.MAX_MORAL_DEPORTISTAS
        elif value < p.MIN_MORAL_DEPORTISTAS:
            self.__moral = p.MIN_MORAL_DEPORTISTAS
        else:
            self.__moral = value

    @property
    def flexibilidad(self):
        return self.__flexibilidad

    @flexibilidad.setter
    def flexibilidad(self, value):
        if value >= p.MAX_FLEXIBILIDAD_DEPORTISTAS:
            self.__flexibilidad = p.MAX_FLEXIBILIDAD_DEPORTISTAS
        elif value < p.MIN_FLEXIBILIDAD_DEPORTISTAS:
            self.__flexibilidad = p.MIN_FLEXIBILIDAD_DEPORTISTAS
        else:
            self.__flexibilidad = value

    @property
    def velocidad(self):
        return self.__velocidad

    @velocidad.setter
    def velocidad(self, value):
        if value >= p.MAX_VELOCIDAD_DEPORTISTAS:
            self.__velocidad = p.MAX_VELOCIDAD_DEPORTISTAS
        elif value < p.MIN_VELOCIDAD_DEPORTISTAS:
            self.__velocidad = p.MIN_VELOCIDAD_DEPORTISTAS
        else:
            self.__velocidad = value

    @property
    def resistencia(self):
        return self.__resistencia

    @resistencia.setter
    def resistencia(self, value):
        if value >= p.MAX_RESISTENCIA_DEPORTISTAS:
            self.__resistencia = p.MAX_RESISTENCIA_DEPORTISTAS
        elif value < p.MIN_RESISTENCIA_DEPORTISTAS:
            self.__resistencia = p.MIN_RESISTENCIA_DEPORTISTAS
        else:
            self.__resistencia = value

    def entrenar(self, atributo, eficiencia):
        # Elegimmos cuanto aumentar
        print(f"\nENTRENANDO A {self.nombre}")
        aumento = p.PUNTOS_ENTRENAMIENTO * eficiencia
        self.moral += p.AUMENTO_MORAL_POR_ENTRENAMIENTO
        if atributo == "0":
            self.velocidad += aumento
            print(f"Velocidad mejorada a {self.velocidad}")
        elif atributo == "1":
            self.resistencia += aumento
            print(f"Resistencia mejorada a {self.resistencia}")
        elif atributo == "2":
            self.flexibilidad += aumento
            print(f"Flexibilidad mejorada a {self.flexibilidad}")

    def lesionarse(self, riesgo):
        probab = uniform(0, 1)
        probab = round(probab, 1)
        if probab <= riesgo:
            print(f"{self.nombre} se ha lesionado durante la competencia!")
            self.lesionado = True
