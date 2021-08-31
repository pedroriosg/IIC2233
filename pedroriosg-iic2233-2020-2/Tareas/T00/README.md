# Tarea 00: DCCombateNaval :school_satchel:

## Consideraciones generales :octocat:

* Según las revisiones que hice, el juego funciona perfectamente.

* En relación al uso de PEP8, tuve problemas a la hora de acortar líneas que tuvieran más de 100 caracteres, ya que mis nombres de las funciones era muy largos. Sin embargo, acorté la mayor cantidad de líneas que pude.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Inicio del Programa:
    * Menú de Inicio: contiene todas las opciones pedidas del enunciado: COMPLETO
    * Funcionalidades: el usuario puede elegir un apodo correctamente con las respectivas restricciones, si ingresa uno válido se dan las opciones pedidas en el enunciado. Se puede comenzar una nueva partida y se da la opcion de elegir el tablero (a prueba de errores). Se puede salir del progama de manera correcta: COMPLETO
    * Puntajes: se muestran los puntajes de los usuarios ordenados como se pide en el enunciado: COMPLETO

* Flujo del Juego:
    * Menú de Juego: contiene las opciones mínimas del enunciado. COMPLETO
    * Tablero: el tablero se genera correctamente de acuerdo a las dimensiones ingresadas, se visualizan los barcos del jugador y enemigo según lo pedido, y se actualiza correctamente después de cada turno: COMPLETO
    * Turnos: al acertar el disparo se marca la celda tanto del jugador con el oponente con una F, además, repite turno. Al errar se marca con una X y finaliza el turno: COMPLETO
    * Bombas: bombas regulares bien implementadas. Las tres bombas especiales generan el efecto deseado y respetan el radio de explosión. Solo se puede usar una bomba especial por partida y no se puede volver a disparar lugares en donde ya se disparó: COMPLETO
    * Barcos: los barcos se distribuyen de manera aleatoria en el tablero. La ejecución se produce en el módulo ```principal.py```línea 38. La función encargada de la ejecución se encuentra en ```funciones.py```linea 122. Se usa ```randint```en las líneas 128 y 139. Los barcos no se traslapan ni se ubican afuera del tablero: COMPLETO
    * Oponente: el oponente juega de manera automática siguiendo las relgas del jugador. El oponente no lanza bombas especiales. Se imprimen las coordenadas de disparo según el enunciado: COMPLETO

* Término del Juego:
    * Fin del Juego: el juego finaliza si se destruyen todos los barcos de alguno de los dos jugadores o cuando un jugador se rinde: COMPLETO
    * Puntajes: el puntajes se clacula de manera correcta y se almacena donde corresponde. En el módulo ```principal.py```en las líneas 88 y 115 se llama a la funcion para calcular puntaje. En el módulo ```funciones.py``` en la función ```calcular_puntaje()```línea 161 se calcula el puntaje: COMPLETO

* Archivos:
    * Manejo de Archivos: se escribe el puntaje de una partida correctamente en el archivo ```puntajes.txt```y se carga correctamente el archivo. En el módulo ```principal.py```en las líneas 91 y 119, se llama a la funcion ```ìnscribir_puntaje()```, la cual esta implementada en el módulo ```funciones.py```en la línea 182: COMPLETO
    * PD: si el archivo ```puntajes.txt``` está vacío, el primer puntaje se inscribe en la línea 2 del archivo. Esto, ya que la función agrega usuarios y puntajes con un \n al inicio.

* General:
    * Menús: los menús son a todo tipo de prueba: COMPLETO
    * Parámetros: se utilizan los parametros entregados y se importa el módulo correctamente. Se utilizan en el módulo ```funciones.py```en la función ```abrir_parametros()```en la línea 169. Luego se utilizan estos valores en otras funciones: COMPLETO
    * Módulos: el programa se encuentra bien modularizado: COMPLETO. 
    * PD: el programa se ejecuta en ```principal.py```y el cual importa a los módulos ```funciones.py```y ```funciones_2.py```. Esto lo hace en las líneas 1 y 2.
    * PEP8: INCOMPLETO. El programa contiene algunas líneas con más de 100 caracteres. Hubo muchas líneas que no pude acortar ya que hubiese tenido que cambiar los nombres descriptivos de las funciones; sin embargo, traté de acerlo en la mayor cantidad posible. El resto, todo ok.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```principal.py```. Este contiene el flujo principal del programa (control de flujo). Maneja las opciones que se ingresan en cada Menú.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```randint()```
2. ```string```: ```ascii_uppercase```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```funciones.py```: El módulo contiene a todas las funciones principales que permiten correr el programa. En general, se encuentran en él funciones que manejan los distintos "Menús", las que leen los distintos archivos (en particular ```tablero.py```, ```parametros.py```y ```puntajes.txt```). Además, en este módulo se incluye la jugada del oponente.
2. ```funciones_2.py```: El módulo contiene a las bombas especiales (Bomba Cruz, Bomba X y Bomba Diamante), adicional a eso, incluye una funcion que se utiliza dentro de la Bomba Diamante.
3.  ```tablero.py```: este módulo lo entregaban en la tarea. Es externo a mi código (por eso lo puse acá). Permite imprmir el tablero en un formato adecuado.
4. ```parametros.py```: este módulo entrega el número de barcos por partida y el radio de explosión de las bombas. Lo entregaron junto con el enunciado.
5. ```puntajes.txt```: en este módulo se agrega el apodo y puntaje de cada usuario que inicia una partida. El módulo lo entregaron junto con el enunciado, y va cambiando a medida que se agregan partidas en el juego.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En general, no realicé supuestos adicionales. Se puede decir que supuse que el jugador Oponente siempre intentará disparar a una coordenada dentro del tablero, creo que es válido porque le aporta fluidez al programa y disminuye potenciales errores de código.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist: este ordena una lista de listas de acuerdo a un parámetro específico y está implementado en el archivo funciones.py en las líneas 46 y ordena a los jugadores de acuerdo a su puntaje del juego, quienes están guardados en una lista de listas.
