from estudiante import cargar_datos, cargar_datos_corto


def verificar_numero_alumno(alumno):  # Levanta la excepción correspondiente
    atributo = alumno.n_alumno
    year = str(alumno.generacion)
    verificar_ano = year[2:]
    codigo = atributo[2:4]
    if not atributo.isnumeric():
        if atributo[len(atributo) - 1] != "J":
            raise ValueError("El numero de alumno es incorrecto")
    if atributo[0:2] != verificar_ano:
        raise ValueError("El numero de alumno es incorrecto")
    if alumno.carrera == "Ingeniería":
        if codigo != "63":
            raise ValueError("El numero de alumno es incorrecto")
    if alumno.carrera == "College":
        if codigo != "61":
            raise ValueError("El numero de alumno es incorrecto")


def corregir_alumno(estudiante):  # Captura la excepción anterior
    try:
        verificar_numero_alumno(estudiante)
        print(f"{estudiante.nombre} está correctamente inscrite en el curso, todo en orden...\n")

    except ValueError as error:
        print(error)
        # Corregir letra
        final = ""
        letra = " "
        for caracter in estudiante.n_alumno:
            if caracter.isnumeric():
                final += caracter
            else:
                letra = "J"
        if letra != " ":
            final += letra
        final = final[4:]
        year = str(estudiante.generacion)
        digito = year[2:]
        if estudiante.carrera == "Ingeniería":
            codigo = "63"
        else:
            codigo = "61"
        final = digito + codigo + final
        estudiante.n_alumno = final
        print(f"{estudiante.nombre} está correctamente inscrite en el curso, todo en orden...\n")

# ************


def verificar_inscripcion_alumno(n_alumno, base_de_datos):  # Levanta la excepción correspondiente
    if n_alumno not in base_de_datos:
        raise KeyError("El numero de alumno no se encuentra en la base de datos.")
    else:
        return base_de_datos[n_alumno]


def inscripcion_valida(estudiante, base_de_datos):  # Captura la excepción anterior
    try:
        verificar_inscripcion_alumno(estudiante.n_alumno, base_de_datos)
    except KeyError as error:
        print(error)
        print("¡Alerta! ¡Puede ser Dr. Pinto intentando atraparte!\n")


# ************

def verificar_nota(alumno):  # Levanta la excepción correspondiente
    nota = alumno.promedio
    if not isinstance(nota, float):
        raise TypeError("El promedio no tiene el tipo correcto")


def corregir_nota(estudiante):  # Captura la excepción anterior
    try:
        verificar_nota(estudiante)
        print(f"Procediendo a hacer git hack sobre {estudiante.promedio}...\n")

    except TypeError as error:
        print(error)
        numero = str(estudiante.promedio)
        if len(numero) >= 3:
            a = numero[0]
            b = numero[2]
            c = "."
            numero = a + c + b
        promedio_final = float(numero)
        estudiante.promedio = promedio_final
        print(f"Procediendo a hacer git hack sobre {estudiante.promedio}...\n")


if __name__ == "__main__":
    datos = cargar_datos_corto("alumnos.txt")  # Se cargan los datos
    for alumno in datos.values():
        if alumno.carrera != "Profesor":
            corregir_alumno(alumno)
            inscripcion_valida(alumno, datos)
            corregir_nota(alumno)
