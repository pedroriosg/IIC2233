import os


def reparar_imagen(ruta_entrada, ruta_salida):
    #--- COMPLETAR ---#
    with open(ruta_entrada, "rb") as bytes_file:
        bytes_read = bytes_file.read()
        bytes_corregidos = bytearray()
        for i in range(0, len(bytes_read), 32):
            chunk = bytearray(bytes_read[i: i + 32])
            if chunk[0] == 1:
                # Se invirtieron
                invertir = chunk[:16]
                invertir = invertir[::-1]
                nuevo_chunk = invertir
                bytes_corregidos += nuevo_chunk
            else:
                bytes_corregidos += chunk[:16]
        archivo = open(ruta_salida, "wb")
        archivo.write(bytes_corregidos)
        archivo.close()


#--- NO MODIFICAR ---#
def reparar_imagenes(carpeta_entrada, carpeta_salida):
    for filename in os.listdir(os.path.join(os.getcwd(), carpeta_entrada)):
        reparar_imagen(
            os.path.join(os.getcwd(), carpeta_entrada, filename),
            os.path.join(os.getcwd(), carpeta_salida, filename)
        )


if __name__ == '__main__':
    try:
        reparar_imagenes('corruptas', 'caratulas')
        print("Imagenes reparadas (recuerda revisar que se carguen correctamente)")
    except Exception as error:
        print(f'Error: {error}')
        print("No has podido reparar las caratulas :'c")
