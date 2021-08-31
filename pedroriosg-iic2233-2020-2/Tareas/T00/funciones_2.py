# En este archivo, las bombas especiales


def bomba_cruz(tab_rival, radio, fila, columna, descubiertos):
    puntos = descubiertos
    repite = False
    dimension = radio - 1
    tabler = tab_rival
    x = fila
    y = columna
    coordenadas_alcance = [[fila, columna]]
    if dimension >= 0:
        # Norte
        fil = x - 1
        for indice in range(dimension):
            if fil >= 0:
                coordenadas_alcance.append([fil, y])
                fil -= 1
        # Sur
        fil = x + 1
        for indice in range(dimension):
            if fil < len(tabler):
                coordenadas_alcance.append([fil, y])
                fil += 1
        # Este
        col = y - 1
        for indice in range(dimension):
            if col >= 0:
                coordenadas_alcance.append([x, col])
                col -= 1
        # Oeste
        col = y + 1
        for indice in range(dimension):
            if col < len(tabler[0]):
                coordenadas_alcance.append([x, col])
                col += 1
        for coordenada in coordenadas_alcance:
            if tabler[coordenada[0]][coordenada[1]] == " ":
                tabler[coordenada[0]][coordenada[1]] = "X"
            elif tabler[coordenada[0]][coordenada[1]] == "B":
                repite = True
                tabler[coordenada[0]][coordenada[1]] = "F"
                puntos += 1
    return tabler, puntos, repite


def bomba_x(tab_rival, radio, fila, columna, descubiertos):
    puntos = descubiertos
    repite = False
    dimension = radio - 1
    tabler = tab_rival
    x = fila
    y = columna
    coordenadas_alcance = [[fila, columna]]
    if dimension >= 0:
        # Diagonal superior derecha
        fil = x - 1
        col = y + 1
        for indice in range(dimension):
            if fil >= 0 and col < len(tabler[0]):
                coordenadas_alcance.append([fil, col])
                fil -= 1
                col += 1
        # Diagonal superior izquierda
        fil = x - 1
        col = y - 1
        for indice in range(dimension):
            if fil >= 0 and col >= 0:
                coordenadas_alcance.append([fil, col])
                fil -= 1
                col -= 1
        # Diagonal inferior derecha
        fil = x + 1
        col = y + 1
        for indice in range(dimension):
            if col < len(tabler[0]) and fil < len(tabler):
                coordenadas_alcance.append([fil, col])
                fil += 1
                col += 1
        # Diagonal inferior izquierda
        fil = x + 1
        col = y - 1
        for indice in range(dimension):
            if col >= 0 and fil < len(tabler):
                coordenadas_alcance.append([fil, col])
                fil += 1
                col -= 1
        for coordenada in coordenadas_alcance:
            if tabler[coordenada[0]][coordenada[1]] == " ":
                tabler[coordenada[0]][coordenada[1]] = "X"
            elif tabler[coordenada[0]][coordenada[1]] == "B":
                repite = True
                tabler[coordenada[0]][coordenada[1]] = "F"
                puntos += 1
    return tabler, puntos, repite

# Esta funcion se usa en Bomba Diamante


def linea(tab_rival, radio, fila, columna, lista):
    dimension = radio - 1
    tabler = tab_rival
    x = fila
    y = columna
    coordenadas_alcance = lista
    coordenadas_alcance.append([x, y])
    if dimension >= 0:
        # Este
        col = y - 1
        for indice in range(dimension):
            if col >= 0:
                coordenadas_alcance.append([x, col])
                col -= 1
        # Oeste
        col = y + 1
        for indice in range(dimension):
            if col < len(tabler[0]):
                coordenadas_alcance.append([x, col])
                col += 1
    return coordenadas_alcance


def bomba_diamante(tab_rival, radio, fila, columna, descubiertos):
    limite = True
    repite = False
    puntos = descubiertos
    r = radio
    t = tab_rival
    x = fila
    y = columna
    coordenadas_alcance = []
    while limite:
        coordenadas = linea(t, r, x, y, coordenadas_alcance)
        coordenadas_alcance = coordenadas
        x -= 1
        r -= 1
        if x < 0 or r < 1:
            limite = False
    limite = True
    r = radio - 1
    t = tab_rival
    x = fila + 1
    y = columna
    while limite and radio != 1:
        coordenadas = linea(t, r, x, y, coordenadas_alcance)
        coordenadas_alcance = coordenadas
        x += 1
        r -= 1
        if x >= len(t) or r < 1:
            limite = False
    for coordenada in coordenadas_alcance:
        if t[coordenada[0]][coordenada[1]] == " ":
            t[coordenada[0]][coordenada[1]] = "X"
        elif t[coordenada[0]][coordenada[1]] == "B":
            repite = True
            t[coordenada[0]][coordenada[1]] = "F"
            puntos += 1
    return t, puntos, repite
