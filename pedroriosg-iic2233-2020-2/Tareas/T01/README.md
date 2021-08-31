# Tarea 01: DCCumbre Olímpica :trophy:

## Consideraciones generales :octocat:

* Según las revisiones que hice, el programa funciona bien.
* La delegacion enemiga no realiza acciones en su día de entrenamiento.
* El programa si bien realiza lo pedido en el enunciado, a la hora de competir carece de prints, solo se muestran algunos eventos que pasan.
* Considere que a la hora de elegir los deportistas es mejor mostrar una vez el equipo disponible para luego dar la opción de ingresar a los competidores. Esto hace que lo que se muestra en consola sea más limpio y claro, y no tan repetitivo.
* A la hora de mostrar el estado de las delegaciones, los atributos de los deportistas están redondeados al entero más cercano, esto para que la tabla no pierda el formato del orden.


### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Programacion Orientada a Objetos:**
    * **Diagrama:**
        * El diagrama respeta el formato solicitado: COMPLETO
        * El diagrama contiene suficientes clases para modelar las entidades y funcionalidades pedidas. Cada clase contiene atributos y métodos respectivos para modelar el programa: COMPLETO
        * El diagrama contiene relaciones (agregación, composición y herencia) entre las clases incluidas, y mantiene consistencia de modelación: COMPLETO
        * Observación: en el diagrama, los metodos abstractos, los parametros que recibe y los que retorna, están especificados en la ```clase Padre``` y no en cada subclase (todas las subclases se comportan de igual manera).
    * **Definición de clases, atributos y métodos:**
        * Las Delegaciones están bien modeladas: COMPLETO. En el módulo ```delegaciones.py```, se modela la clase abstracta ```class Delegaciones()```(linea 6), y las subclases, ```class IEEEsparta()```(linea 161) y ```class DCCrotona()```(linea 181). 
        * Los Deportistas están bien modelados: COMPLETO. En el módulo ```deportistas.py```, se modela la clase ```class Deportistas()```(linea 5)
        * Los Deportes están bien modelados: COMPLETO. En el módulo ```deportes.py```, se modela la clase abstracta ```class Deportes()```(linea 5), y las subclases, ```class Atletismo()```(linea 93), ```class Natacion()```(linea 131), ```class Gimnasia()```(linea 169) y ```class Natacion()```(linea 207)
        * El Campeonato está bien modelado: COMPLETO. En el módulo ```campeonato.py```, se modela la clase ```class Campeonato()``` (linea 7)
    * **Relaciones entre clases:**
        * Se utilizan clases abstractas cuando corresponde: COMPLETO. Las clases abstractas son ```class Delegaciones()```(módulo ```delegaciones.py```(linea 6) y ```class Deportes()```(modulo ```deportistas.py```(linea 5)).
        * Utiliza consistentemente relaciones de agregación y composición: COMPLETO. Se puede notar que el campeonato es el que le da vida a las delegaciones y a los deportes, si se acaba el campeonato, nada tiene sentido (relacion de composición). Ademas, se puede ver que en la ```class Delegaciones()```en el atributo ```equipo```(módulo ```delegaciones.py```(linea 11)) existe una relación de agregación, ya que este atributo es una lista de instacias de la clase ```deportistas.py```.

* **Partidas:**
    * **Crear partidas:**
        * Se pueden crear una o más simulaciones para la DCCumbre Olímpica: COMPLETO. Se pueden crear todas las simulaciones que uno quiera (con un mismo nombre de entrenador, y por lo tanto, un mismo equipo). Si se quiere cambiar de usuario y delegación se debe volver al Menú de Inicio a través del Menú Principal.
        * Se permite elegir el tipo de Delegación e ingresar el nombre de los entrenadores, respetando las restricciones establecidas: COMPLETO.
        * Se instancia correctamente la Delegación seleccionada, considerando los valores iniciales de sus atributos: COMPLETO. En el módulo ```main.py```, linea 22, se llama a la función ```instalar_delegaciones(...)```, está funcion, definida en el módulo ```funciones.py``` en la linea 51, instancia las delegaciones con los respectivos nombres y elección de Delegación del usuario.
        * Se instancia correctamente los Deportistas asociados a las Delegaciones, considerando los valores iniciales de sus atributos: En el módulo ```main.py```, linea 20, se llama a la función ```datos_deportistas()```, está funcion, definida en el módulo ```funciones.py``` en la linea 5, instancia los deportistas para luego incoroporarlos a las delegaciones.
    * **Guardar:**
        * Se actualiza correctamente la información diaria de los resultados en los archivos correspondientes: COMPLETO. Esto se realiza en el archivo que el programa crea ```resultados.txt```. El archivo se "renueva" cada vez que comienza una nueva simulación.

* **Acciones:**
    * **Delegaciones:**
        * Se puede fichar un deportista, en caso de poder hacerlo se agrega al equipo de la delegación. Si no puede fichar se avisa en consola: COMPLETO
        * Se puede escoger un Deportista para entrenar, en caso de poder hacerlo se aplican correctamente los aumentos de los atributos correspondientes: COMPLETO
        * Se implementa la posibilidad de recuperación de una lesión. Posee un método adecuado que permite una correcta modelación del evento: COMPLETO. En el módulo ```delegaciones.py```, método ```sanar_lesiones()```linea 106, se implementa esta opción. Se calcula una probabilidad de lesión según fórmula, luego se redondea y se compara con un número aletario también redondeado. Si el número generado cae bajo o igual a la probabilidad de sanarse, entonces se sana.
        * Puede comprar tecnología y aumenta correctamente sus atributos asociados: COMPLETO.
        * Se implementa correctamente la habilidad especial según el tipo de delegación. La puede utilizar sólo una vez por simulación: COMPLETO. En el módulo ```delegacion.py```se define como un ```abstractmethod()```el método ```habilidad_especial()```, para la IEEEsparta, linea 172, y para la DCCrotona, linea 192. La cantidad de veces que se puede ejecutar está controlada por un booleano en ```main.py``` llamado ```habilidad_especial```definido en la linea 10.
        * Descuenta correctamente las DCCOIns de las Delegaciones cada vez que se ejecuta una acción que implica costo: COMPLETO. En el módulo ```delegaciones.py```, al fichar deportistas (linea 55), al entrenar deportistas (linea 92), al sanar deportistas (linea 126 y 128), al comprar tecnología (linea 146) y al usar la habilidad especial (IEEEsparta, linea 178; DCCrotona, linea 198)
        * Se aumentan y descuentan correctamente los beneficios especiales asociados a cada delegación: COMPLETO.
            * **IEEEspartanos:** Entrenamiento x 1.7 (```delegaciones.py```linea 95, ```deportistas.py```linea 72). Moral disminuye al doble (```campeonato.py```linea 196)
            * **DCCrotona:** Pago doble por lesion (```delegaciones.py```linea 126). Aumento doble moral por ganador (```campeonato.py```linea 193)
    * **Deportistas:**
        * Se implementa correctamente el entrenamiento de los deportistas, respetando el parametro correspondiente.(PUNTOS_ENTRENAMIENTO): COMPLETO. En el módulo ```deportistas.py```en la linea 72.
        * Los deportistas pueden lesionarse: los deportistas pueden lesionarse solo si la competencia es válida. Esto se realiza en las siguientes lineas del módulo ```campeonato.py```: 72, 73, 100, 101, 128, 129, 156, 157. En esas lineas se llama a la funcion ```leisonarse``` del módulo ```deportistas.py```linea 84.
        * Se calcula correctamente la probabilidad de lesión para cada competencia: COMPLETO. En el módulo ```deportistas.py```linea 87, se compara un número al azar con la probabilidad de riesgo, de esta manera, vemos si se lesiona. Esta idea está sacada de la Issue # 386. Si el numero generado es menor o igual al riesgo, el jugador se lesiona.
        * Se pueden visualizar bien sus datos en la delegación, y al momento de ficharlos: completo. Al momento de fichar se debe escribir el nombre exacto del deportista a fichar, esto ya que están almacenados en un diccionario.
    * **Competencia:**
        * Se implementa y calcula correctamente la validez de una competencia: SEMI - COMPLETO: En el módulo ```deportes.py```en la linea 11, se define el módulo para validar la competencia. Este módulo presenta un control de flujo a base de if - elif y else, que funciona según las pruebas que hice y creo que cubre todos los casos posibles. La validez de la competencia se chequea antes de competir, si es válida la competencia, se da la opción a los deportistas de lesionarse y se chequea nuevamente. Digo que está semi - completo ya que no lo probé suficientes veces, y los ```prints```que hay en el programa no son lo suficientemente descriptivos. Sin embargo, está la posibilidad de que funcione a la perfección.
        * Se implementa y calcula de forma correcta el ganar de una competencia: COMPLETO. Si la competencia es válida, se calcula al ganador. Esto se hace según el deporte. En el modulo ```deportes.py```en las lineas 99, 137, 175 y 213 están los métodos que realizan esto, según lo especificado en el enunciado.
        * Se le ofrecen al entrenador las opciones correctas de deportistas que puede escoger para cada competición: COMPLETO. El entrenador puede elegir a cualquier deportista para competir en cualquier competencia, pero él tiene conocimiento de sus atributos y su estado de lesion.
        * Se le asigna una medalla de ganador a cada delegación ganadora de una prueba. Se aplican las bonificaciones y descuentos de moral, excelencia, respeto y DCCoins: COMPLETO. Esto pasa en el módulo ```campeonato.py```en el método ```premiar```linea 81.
        * Luego de terminar las competencias del día, se pasa al día siguiente: COMPLETO. Módulo ```campeonato.py```linea 178
        * Se muestra correctamente el estado de cada Delegación, el estado de sus integrantes, y el estado de la Competencia, con toda la información especificada en el enunciado: COMPLETO.
        * Se determina correctamente a la Delegación ganadora de la DCCumbre Olímpica: COMPLETO. Módulo ```main.py```linea 82, en esa linea comienza el control de flujo que determina al ganador.
        * Se calcula correctamente la moral de cada delegación al inicio de cada día, y se muestra en consola: COMPLETO. El método encargado de esto se encunetra en el módulo ```campeonato.py```en la línea 198. Además, este método se llama en el módulo ```main.py```en las lineas 39 y 80.
* **Consola:**
    * **Menu de Inicio:**
        * El menú contiene las opciones mínimas pedidas: COMPLETO.
    * **Menu Principal:**
        * El menú contiene las opciones mínimas pedidas: COMPLETO
    * **Menu Entrenador:**
        * El menú contiene las opciones mínimas pedidas: COMPLETO
    * **Menu de Entrenar:**
        * El menú contiene las opciones mínimas pedidas: COMPLETO. El Menú de Entrenador no funciona como un Menú, sino que se le pide secuencialemente el número del jugador a entrenar, y una vez seleccionado, su atributo.
    * **Opciones Mínimas:**
        * Visualiza los resumenes de todos los eventos del día que se mencionan en el enunciado: COMPLETO
    * **Robustez:**
        * Todos los menús son a prueba de cualquier tipo de input: COMPLETO. Segun las pruebas que hice, son a prueba de cualquier input.
    
* **Manejo de archivos:**
    * **Archivos CSV:**
        * Trabaja correctamente con todos los archivos CSV entregados: COMPLETO. Trabajé con los archivos .csv entregados por primera vez (los con espacios). En el archivo delegaciones.csv, probé cambiando el header y me funcionó. En el archivo deportistas.csv, probe con el archivo sin espacios y me funcionó, aunque mi programa está hecho para el primer archivo (el con espacios). Sobre este archivo no probé un cambio de header. Se trabaja con ambos archivos en el módulo ```funciones.py```en ambas funciones definidas. Específicamente en las lineas 9 y 54.
    * **```parametros.py```:**
        * Utiliza e importa correctamente parametros.py: COMPLETO. Se importa correctamente en los módulos necesarios. (aunque para simplicar, lo importo ```import parametros as p```). Ubicado en las primeras lineas de cada módulo. ```deportes.py```(linea 1), ```campeonato.py```(linea 2), ```main.py```(linea 4), ```deportistas.py```(linea 1), ```delegaciones.py```(linea 1).
        * Archivo parametros.py contiene todos los parámetros especificados en el enunciado: COMPLETO. Observacion: con respecto al riesgo del deporte, el cual es un parámetro, se asume que al momento de definirlo en ```parametros.py```se define como un float entre 0 y 1.
    * **```resultados.txt```:**
        * El archivo resultados.txt presenta todo lo pedido en el enunciado, en el orden correcto: COMPLETO.



## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Este contiene el flujo principal del programa (control de flujo). Maneja las opciones que se ingresan en cada Menú y controla la cantidad de días que dura la competencia. Además, en él se instancian a los deportistas y a las delegaciones con sus respectivos entrenadores.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```uniform()```, ```choice()```
2. ```abc```: ```ABC```, ```abstractmethod()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros.py```: el módulo contiene todos los parámetros que se usan a lo largo del programa (60 aproximadamente)
2. ```funciones_bitacora.py```: el módulo contiene todas las funciones relacionadas con el archivo ```resultados.txt``` que se crea cuando se ejecuta el módulo principal. Como por ejemplo, crear el archivo, agregar el día de la competencia y los respectivos resultados de las competencias.
3.  ```funciones.py```: este módulo contiene dos funciones, una que lee los deportistas del archivo ```deportistas.csv```entregado, y los instancia; otro que instancia a las delegaciones con sus respectivos entrenadores.
4. ```menus.py```: este módulo contiene los menus mínimos pedidos en el enunciado, dentro del archivo hay una funcion para cada menú, el cual maneja posibles errores de ```input()```.
5. ```deportistas.py```: este módulo contiene a la ```class Deportistas()```y todos sus métodos.
6. ```deportes.py```: este módulo contiene a la clase abstracta ```class Deportes(ABC)```y todos los deportes, los cuales son clases que hereden de ```class Deportes(ABC)```. Las deportes son: ```class Atletismo()```, ```class Natacion()```, ```class Gimnasia()``` y ```class Cicilismo()```.
7. ```delegaciones.py```: el módulo contiene a la clase abstracta ```class Delegaciones(ABC)```, y también las subclases de esta, ```class IEEEsparta()``` y ```class DCCrotona()```.
8. ```campeonato.py```: este modulo contiene a la clase ```class Campeonato()```y todos sus métodos.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En general, no realicé supuestos adicionales.

## Referencias de código externo :book:

Para esta tarea no utilicé código externo.
