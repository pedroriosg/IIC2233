from collections import namedtuple, defaultdict


# Para esta parte necesitarás los contenidos de la semana 0


def cargar_datos(path):
    # Para esta función te puede servir el cuaderno 3 de la semana 0
    with open(path, "rt") as archivo:
        informacion = archivo.readlines()

    # Limpiamos la información
    ayudantes = list()
    for linea in informacion:
        ayudante = linea.strip().split(",")
        ayudantes.append(ayudante)
    ayudantes = ayudantes[1:]
    return ayudantes


# De aquí en adelante necesitarás los contenidos de la semana 1


def crear_ayudantes(datos):
    # Completar función
    lista_ayudantes = []
    Ayudante = namedtuple("Ayudante", ["nombre", "cargo", "usuario"])
    for dato in datos:
        ayudante = Ayudante(dato[0], dato[1], dato[2])
        lista_ayudantes.append(ayudante)
    return lista_ayudantes


def encontrar_cargos(ayudantes):
    # Completar función
    set_cargos = {a.cargo for a in ayudantes}
    return set_cargos


def ayudantes_por_cargo(ayudantes):
    # Completar función
    diccionario = dict()
    for ayudante in ayudantes:
        if ayudante.cargo not in diccionario:
            diccionario[ayudante.cargo] = list()
        diccionario[ayudante.cargo].append(ayudante)
    return diccionario


if __name__ == '__main__':
    datos = cargar_datos('ayudantes.csv')
    if datos is not None:
        print('Se lograron leer los datos')
    else:
        print('Debes completar la carga de datos')

    ayudantes = crear_ayudantes(datos)
    if ayudantes is not None:
        print('\nLos ayudantes son:')
        for ayudante in ayudantes:
            print(ayudante)
    else:
        print('\nDebes completar la creación de Ayudantes')

    cargos = encontrar_cargos(ayudantes)
    if cargos is not None:
        print('\nLos cargos son:')
        for cargo in cargos:
            print(cargo)
    else:
        print('\nDebes completar la búsqueda de Cargos')

    clasificados = ayudantes_por_cargo(ayudantes)
    if clasificados is not None:
        print('\nLos ayudantes por cargos son:')
        for cargo in clasificados:
            print(f'\n{cargo}')
            for ayudante in clasificados[cargo]:
                print(ayudante)
    else:
        print('\nDebes completar la clasificación de Ayudantes')
