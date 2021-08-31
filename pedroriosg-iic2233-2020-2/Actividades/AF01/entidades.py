class Criatura:

    def __init__(self, nombre, tipo, hp, atk, sp_atk, defense):
        # Completar
        self.nombre = nombre
        self.tipo = tipo
        self.__hp = hp
        self.hp_base = hp
        self.atk = atk
        self.sp_atk = sp_atk
        self.defense = defense
        self.preferencia = self.preferencia_combate()

    # Recuerda completar las properties del atributo privado para el hp
    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self.__hp = 0
        elif value > self.hp_base:
            self.__hp = self.hp_base

    def preferencia_combate(self):
        # Completar
        if len(self.tipo) > 5:
            return "Especial"
        else:
            return "Fisico"

    def recibir_ataque(self, dano):
        # Completar
        self.hp -= dano
        pass

    def __str__(self):
        # Completar
        mensaje = f"Me llamo {self.nombre} y soy de tipo {self.tipo}"
        return mensaje


class Entrenador:

    def __init__(self, nombre, bolsillo):
        # Completar
        self.nombre = nombre
        self.bolsillo = bolsillo


if __name__ == "__main__":
    # NO MODIFICAR
    # El siguiente codigo te ayudara a hacer debugging,
    # simplemente ejecútalo para ver cómo vas

    # Instancias de Criatura
    criatura_alonso = Criatura("Alonso", "Water", 100, 100, 100, 100)
    criatura_juan = Criatura("Juan", "Normal", 90, 90, 90, 90)
    criatura_lucas = Criatura("Lucas", "Ground", 90, 90, 90, 90)

    # Aqui llamaremos a todos los atributos de la clase Criatura
    # si faltan atributos se indicara un mensaje de error
    # (Veremos try/except en profundidad más adelante en el curso)
    try:
        criatura_alonso.nombre
        criatura_alonso.tipo
        criatura_juan.hp
        criatura_juan.atk
        criatura_lucas.sp_atk
        criatura_lucas.defense
        print("Atributos de Criatura: OK")
    except AttributeError as error:
        print(f"Aún no completas los atributos de Criatura ({error})")

    # Aquí se prueba si el método preferencia_combate esta correctamente implmentado
    if criatura_alonso.preferencia_combate() != "Fisico" or criatura_juan.preferencia_combate() != "Especial":
        print("El método preferencia_combate aún no esta completado correctamente")
    else:
        print("Método preferencia_combate de Criatura: OK")

    # Aquí se prueba si el método recibir_ataque esta correctamente implmentado
    try:
        criatura_juan.recibir_ataque(100)
        if criatura_juan.hp != 0:
            print("El método recibir_ataque aún no esta completado correctamente")
        else:
            print("Método recibir_ataque de Criatura: OK")
    except AttributeError as error:
        print(f"Aún no completas el atributo hp de Criatura ({error})")

    # Instancia de Entrenador
    entrenador_jose = Entrenador("Jose", None)

    # Aqui llamaremos a todos los atributos de la clase Entrenador
    # si faltan atributos se indicara un mensaje de error
    try:
        entrenador_jose.nombre
        entrenador_jose.bolsillo
        print("Atributos de Entrenador: OK")
    except AttributeError as error:
        print("Aún no completas los atributos de Entrenador")
