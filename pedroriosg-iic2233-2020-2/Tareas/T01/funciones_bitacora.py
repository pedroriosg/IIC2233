def crear_txt():
    archivo = open("resultados.txt", "w")
    archivo.close()
    archivo = open("resultados.txt", "a")
    archivo.write("RESULTADOS DÍA A DÍA DCCUMBRE OLÍMPICA\n")
    archivo.write(38 * "-")
    archivo.close()


def agregar_bitacora(competencia, dele_ganadora, depo_ganador):
    archivo = open("resultados.txt", "a")
    archivo.write(f"\nCompetencia: {competencia}")
    archivo.write(f"\nDelegacion Ganadora: {dele_ganadora}")
    archivo.write(f"\nDeportista Ganador: {depo_ganador}\n")
    if competencia == "Ciclismo":
        archivo.write("\n" + 38 * "-")
    archivo.close()


def agregar_dia(dia):
    archivo = open("resultados.txt", "a")
    archivo.write(f"\nDia: {dia}\n")
    archivo.close()
