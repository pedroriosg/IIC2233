from abc import ABC, abstractmethod
from parametros import (
    BONOS_CASA,
    PROBABILIDAD_ABUCHEAR_GRYFFINDOR, PROBABILIDAD_APLAUDIR_GRYFFINDOR,
    PROBABILIDAD_APLAUDIR_SLYTHERIN, PROBABILIDAD_ABUCHEAR_SLYTHERIN,
)
import random


class Programago(ABC):

    # Completar

    def __init__(self, nombre, saludo):
        self.nombre = nombre
        self.saludo = saludo


class Estudiante(Programago, ABC):

    # Completar

    def __init__(self, nombre, saludo):
        super().__init__(nombre, saludo)
        self.valor = 10
        self.inteligencia = 10
        self.lealtad = 10
        self.ambicion = 10

    @abstractmethod
    def abuchear(self):
        pass

    @abstractmethod
    def aplaudir(self):
        pass


class EstudianteGryffindor(Estudiante):

    # Completar

    def __init__(self, nombre, saludo, *args):
        super().__init__(nombre, saludo)
        numero = random.randint(BONOS_CASA["MIN_VALOR_GRYFFINDOR"],
                                BONOS_CASA["MAX_VALOR_GRYFFINDOR"])
        self.valor += numero

    def abuchear(self):
        if random.random() <= PROBABILIDAD_ABUCHEAR_GRYFFINDOR:
            print(self.nombre + ": buuuuuuu!! Abajo Slytherin!!")
            return True
        return False

    def aplaudir(self):
        if random.random() <= PROBABILIDAD_APLAUDIR_GRYFFINDOR:
            print(self.nombre+": *clap clap clap clap*")
            return True
        return False


class EstudianteSlytherin(Estudiante):

    # Completar

    def __init__(self, nombre, saludo, *args):
        super().__init__(nombre, saludo)
        super().__init__(nombre, saludo)
        numero = random.randint(BONOS_CASA["MIN_AMBICION_SLYTHERIN"],
                                BONOS_CASA["MAX_AMBICION_SLYTHERIN"])
        self.ambicion += numero

    def abuchear(self):
        if random.random() <= PROBABILIDAD_ABUCHEAR_SLYTHERIN:
            print(self.nombre + ": buuuuu!! Que mal Gryffindor!!!")
            return True
        return False

    def aplaudir(self):
        if random.random() <= PROBABILIDAD_APLAUDIR_SLYTHERIN:
            print(self.nombre+": *clap clap*")
            return True
        return False


if __name__ == '__main__':
    # Instancias de prueba
    estudiante_gryffindor = EstudianteGryffindor('Pruebardo', 'probando la clase EstudianteGryffindor')
    estudiante_slytherin = EstudianteSlytherin('Pruebina', 'probando la clase EstudianteSlytherin')
    # Pruebas de atributos
    print('Soy ' + estudiante_gryffindor.nombre + ' y estoy ' + estudiante_gryffindor.saludo)
    print('Soy ' + estudiante_slytherin.nombre + ' y estoy ' + estudiante_slytherin.saludo)
    # Pruebas de clases/subclase
    if isinstance(estudiante_gryffindor, Estudiante):
        print('EstudianteGryffindor hereda correctamente de Estudiante!')
    if isinstance(estudiante_slytherin, Estudiante):
        print('EstudianteSlytherin hereda correctamente de Estudiante!')
    if isinstance(estudiante_gryffindor, Programago):
        print('EstudianteGryffindor hereda correctamente de Programago!')
    if isinstance(estudiante_slytherin, Programago):
        print('EstudianteSlytherin hereda correctamente de Programago!')
