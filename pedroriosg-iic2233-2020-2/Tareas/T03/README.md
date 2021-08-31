# Tarea 03: DCColonos :school_satchel:

## Consideraciones generales :octocat:

* En primer lugar, mecionar que utilicé como base y lógica de mi código, el usado en la activdiad formativa 5 (AF05). De ese archivo, saqué ideas de mi código e incluso, hay métodos que están iguales (incluso con los mismos comentarios en los métodos enviar, recibir, codificar y decodificar del Servidor y del Cliente). Si bien el código puede ser difícil de leer, trataré de explicarlo lo mejor posible en este ```README```.

* En segundo lugar, comentar que el código en general funciona bien. Lo único que no está implementado, son los errores de conexión que pueden haber al salirse un cliente, o caer el servidor. Junto con ello, el boton para volver a la sala de espera de la ventana de rankings (ventana final), tampoco funciona.

* Utilicé la librería ```faker``` sugerida en el enunciado.

* Para esta tarea, utilicé la versión 5.13 de PyQt5.

* En relación al uso de PEP8, no tuve problemas (hay una línea con exactamente 100 carácteres), sin embargo no pude comentar el código como me hubiese gustado.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Networking:**

    * **Protocolo:**

        * Correcto uso de TCP/IP: COMPLETO: en ```servidor.py```, linea 33; y en ```cliente.py```, linea 22.
    
    * **Correcto uso de sockets:**

        * Instancia y conecta los sockets de manera correcta: COMPLETO: en ```servidor.py```, linea 34; y en ```cliente.py```, linea 23.
        * Las aplicaciones pueden trabajar concurrentemente sin bloquearse por escuchar un socket: COMPLETO: Se manjea en el método ```aceptar_clientes``` y ```escuchar_clientes``` del módulo ```servidor.py``` (líneas 49 y 80 respectivamente).
    
    * **Conexión:**

        * La conexión es sostenida en el tiempo y de propósito general para todos los tipos de mensajes que pueden intercambiar: COMPLETO
    
    * **Manejo de clientes:**

        * Se pueden conectar múltiples clientes sin afectar el funcionamiento del programa: COMPLETO
        * Se pueden desconectar múltiples clientes, de forma esperada, sin afectar el funcionamiento del programa: INCOMPLETO
        * Se puede desconectar el servidor, de forma inesperada, y los clientes deben manejarlo apropiadamente: INCOMPLETO

    
* **Arquitectura Cliente - Servidor:**

    * **Roles:**

        * Correcta separación de recursos entre Cliente y Servidor: COMPLETO: cada carpeta (```server``` y ```cliente```) tiene su archivo repsectivo ```servidor.py```y ```cliente.py``` los cuales manejan los recursos. En el caso del Servidor, se maneja a través de la clase Lógica (de ```logica.py```) y en el caso del cliente, se manjea a través de la clase Controlador (de ```controlador.py```).
        * Las responsabilidades de cada cliente son consistentes al enunciado: COMPLETO: Envía las acciones a través del Controlador (en ```controladro.py```) donde conecta las señales obtenidas desde la Sala de Juego. Recibe e interpreta las respuestas y actualizaciones que envía el servidor en su método ```manejar_mensaje```.
        * Las responsabilidades del servidor son consistentes al enunciado: COMPLETO: Asigna de manera automática un nombre aleatorio en el método ```crear_nombres``` y ```crear_jugador```del módulo ```logica.py```. Procesa y valida las acciones realizadas por los participantes en el método ```manejar_mensaje```del módulo ```logica.py```. Los cambios los distribuye en tiempo real. Almacena y actualiza información en las respectivas clases que componen el juego, (Catan, Mapa, Caminos, Nodos y Hexagonos)

    * **Consistencia:**

        * Se mantiene coordinada y actualizada la información en todos los clientes y en el servidor: COMPLETO
        * Se utilizan locks cuando es necesario: COMPLETO: Uso locks cuando el servidor pobla de manera al azar el mapa de juego. Esto lo hago en el método ```poblar_servidor```del módulo ```catan.py```en las líneas 36 y 81.
    
    * **Logs:**

        * Se implementan logs del servidor, que permiten visualizar la información indicada en el enunciado: COMPLETO
    
* **Manejo de bytes:**

    * **Codificación:**

        * Se utiliza little y big endian cuando corresponde para transformar a bytes valores enteros: COMPLETO: en ```servidor.py``` en las lineas 117, 124 y 133. En```cliente.py``` en las lineas 64, 71 y 80.
        * Correcta implementación y manejo de la estructura de bytes: COMPLETO: en los métodos  ```enviar.py``` y ```recibir.py``` del módulo ```servidor.py```(lineas 108 y 138). También, en los métodos  ```enviar.py``` y ```recibir.py``` del módulo ```cliente.py```(lineas 54 y 89)

    * **Decodificación:**

        * Se utiliza little y big endian cuando corresponde para transformar de bytes a valores enteros: COMPLETO: en en ```servidor.py``` en la linea 152. En ```cliente.py``` en la línea 100. 
        * Correcta implementación y manejo de la estructura de bytes: COMPLETO: en los métodos  ```enviar.py``` y ```recibir.py``` del módulo ```servidor.py```(lineas 108 y 138). También, en los métodos  ```enviar.py``` y ```recibir.py``` del módulo ```cliente.py```(lineas 54 y 89)
    
    * **Integración:**

        * Utiliza correctamente el protocolo para el envío de mensajes: COMPLETO: En las líneas y métodos en los dos ítems anteriores a este ```README```.
    
* **Interfaz Gráfica:**

    * **Modelación:**

        * Existe una correcta separación entre front-end y back-end en el caso del cliente: COMPLETO: el archivo ```controlador.py``` hace el rol de backend de las ventanas.
    
    * **Sala de Espera:**

        * Se visualiza correctamente la ventana. Se muestran todos los usuarios conectados. La información se actualiza correctamente: COMPLETO
        * En caso de que se conecte un usuario y la partida haya comenzado, se advierte correctamente y se da la opción de finalizar el programa: COMPLETO
    
    * **Sala de Juego:**

        * Se visualizan correctamente la ventana con todos los elementos solicitados en el enunciado. La información se actualiza correctamente para todos los clientes: COMPLETO
        * Se visualiza correctamente el mapa del juego con todos los elementos solicitados en el enunciado. La información se actualiza correctamente para todos los clientes: COMPLETO
        * Se visualiza correctamente el último lanzamiento de dados. La información se actualiza correctamente para todos los clientes: COMPLETO
        * Se visualiza correctamente el jugador actual del turno. La información se actualiza correctamente para todos los clientes: COMPLETO
        * Existe un mecanismo para comprar chozas y caminos. Manda correctamente la información al servidor y este responde apropiadamente. Se actualiza correctamente la interfaz de cada usuario: COMPLETO
        * Existe un mecanismo para comprar las cartas de desarrollo Manda correctamente la información al servidor y este responde apropiadamente. Se actualiza correctamente la interfaz de cada usuario: COMPLETO
        * Cuando se juega una carta de monopolio, se crea una interfaz para elegir la materia prima. Se puede seleccionar la materia prima deseada: COMPLETO
        * Se implementa una ventana para intercambiar recursos. Se puede seleccionar la materia prima del usuario y la del jugador con el cual intercambiar, junto a la cantidad de cada uno. Se puede seleccionar el jugador con el cual intercambiar: COMPLETO
        * En caso de que se realize una acción inválida, existe un mensaje avisando el problema: COMPLETO.
        * Se visualiza correctamente la ventana. Se muestran todos los jugadores y los puntajes. Se informa correctamente si el jugador ganó o perdió la partida: COMPLETO
        * Hay un botón que redirige a la Sala de espera y funciona correctamente: INCOMPLETO

* **Grafo:**

    * **Archivo:**

        * Se instancia correctamente un grafo no dirigido: COMPLETO: (Supongo). Mi clase Mapa del módulo ```mapa.py``` se encarga de instanciar los elementos del grafo y guardarlos en estructuras que puedan ser recorridas para cambiar sus atributos y estados.
    
    * **Modelación:**

        * El grafo se actualiza correctamente según los cambios realizados por los jugadores: COMPLETO: Al ocupar una choza/camino (```verificar```y ```verificar_camino```del archivo ```catan.py``` (lineas 147, 170)) se actualiza el elemento y se marca como ocupado por un jugador.

    * **Funcionalidades:**

        * Se verifica que se cumplen las restricciones correspondientes para construir una choza: COMPLETO: en el método ```verificar``` del módulo ```catan.py```
        * Se verifica que se cumplen las restricciones de contrucción correspondientes para construir una carretera: COMPLETO: en el método ```verificar``` del módulo ```catan.py```
        * Se calcula correctamente la carretera mas larga: COMPLETO: Se usan los métodos ```carretera_mas_larga``` del módulo ```catan.py```. El cual conecta con un método de cada jugador llamado ```calcular_carretera```, de la clase Jugador, que está en el módulo ```jugadores.py``` en la linea 128.
    
* **Reglas del DCColonos:**

    * **Inicio del juego:**

        * Se asigna correctamente una materia prima y un número de ficha a cada hexagono: COMPLETO
        * Se ubican correctamente las chozas y carreteras iniciales de cada jugador en el mapa. Se reparten correctamente los recursos iniciales a cada jugador: COMPLETO
    
    * **Lanzamiento de dados:**

        * Se reparten correctamente los recursos del hexágono correspondiente al número obtenido: COMPLETO
        * En caso de que el número obtenido sea 7, los jugadores con 8 o mas cartas devuelven la mitad de ellas de manera aleatoria al banco: COMPLETO
    
    * **Turno:**

        * Se implementa correctamente la carta de Punto de Victoria. Se verifica que el jugador posea los recursos necesarios para realizar la compra: COMPLETO: metodo ```sacar_carta```de ```catan.py```linea 204. La línea 205 conecta con el método ```verificar_carta``` de cada jugador (```jugadores.py```) que verifica que se posean los recursos necesarios.
        * Se implementa correctamente la Carta de Monopolio. Se verifica que el jugador posea los recursos necesarios para realizar la compra: COMPLETO: método ```obtener_monopolio```de ```catan.py``` linea 217. La línea 205 conecta con el método ```verificar_carta``` de cada jugador (```jugadores.py```) que verifica que se posean los recursos necesarios.
        * Se implementa correctamente el Intercambio con jugadores: COMPLETO
        * Se asignan 2 puntos extras al jugador que tenga la carretera mas larga: COMPLETO
        * Al pasar de turno se calculan los puntos de de victoria de cada jugador: COMPLETO
    
    * **Término de Juego:**

        * Si un jugador alcanza los puntos de victoria necesarios el juego acaba: COMPLETO

* **General:**

    * **Parámetros (JSON):**

        * Todos los parametros se encuentran en alguno de los parametros.json. Se utiliza y carga correctamente parametros.json: COMPLETO: Los parametros se pueden ver en los archivos de cada carpeta. Se cargan los parametros en el método ```leer_parametros_json``` en cual se encuentra en el archivo ```logica.py``` (linea 130) y ```controlador.py``` (linea 172).
    
    * **Grafo (JSON):**

        * Se utiliza y se carga de forma correcta el archivo Grafo.json: COMPLETO: metodo ```leer_parametros_json``` del módulo ```mapa.py```(linea 106)
    
    * **Generador de Mazos:**
        
        * Se utiliza correctamente al función ```sacar_cartas()```, para sacar cartas del mazo. Se importa correctamente la función: COMPLETO: modulo ```catan.py```, metodo ```sacar_carta``` linea (207).

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` de la carpeta ```server```, y luego para cada cliente que desea conectarse, el módulo ```main.py``` de la carpeta ```client```. Los archivos necesarios para que el código funcione son los indicados en la sección **Librerias Propias** (junto con los indicados anteriormente)

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```uic```
2. ```PyQt5.QtWidgets```: ```QApplication```, ```QLabel```, ```QMessageBox```.
3. ```PyQt5.QtGui```: ```QFont```, ```QPixmap```, ```QDrag```, ```QPixmap```, ```QPainter```.
4. ```PyQt5.QtCore```: ```Qt```,```QObject```, ```pyqtSignal```. 
5. ```sys```
6. ```os```
7. ```time```: ```sleep```.
8. ```random```: ```randint```, ```choice```, ```sample```.
9. ```json```
10. ```threading```
11. ```socket```
12. ```faker```: ```Faker```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### QtDesigner

1. ```sala_espera.ui```: Contiene elementos gráficos de la sala de espera.
2. ```sala_espera_warning.ui```: Contiene elementos gráficos de la sala de advertencia que se levanta a quienes se tratan de conectar una vez que el juego ya ha comenzado.
3. ```sala_juego.ui```: Contiene elementos gráficos de la sala de juego.
4. ```ìntercambio.ui```: Contiene elementos gráficos del pop - up que se levanta para negociar con otro jugador.
5. ```solicitud_intercambio.ui```: Contiene elementos gráficos del pop - up que se levanta al tener que aceptar o rechazar el negocio con otro jugador.
6. ```monopolio.ui```: Contiene elementos gráficos que permiten obtener el monopolio de alguna materia prima.
7. ```fin_partida.ui```: Contiene elementos de la ventana con los rankings y puntajes, desplegada una vez que se acaba el juego.

#### Archivos Python Cliente (carpeta ```client```)

* Los archivos ```.ui``` van en esta carpeta. (El módulo ```main.py``` del cliente, también va acá). También la carpeta de ```sprites```va acá.

1. ```frontend_sala_espera.py```: maneja la grafica de la sala de espera y de la ventana de warning.
2. ```frontend_sala_juego.py```: maneja la grafica de la sala de juego.
3.  ```frontend_intercambio.py```: maneja la grafica de la ventana para solicitar un intercambio con otro jugador.
4. ```frontend_solicitud_intercambio.py```: maneja la grafica de la ventana para aceotar o rechazar un intercambio de otro jugador.
5. ```frontend_monopolio.py```: maneja la grafica de la ventana para solicitar el monopolio de alguna materia prima.
6. ```frontend_fin_partida.py```: maneja la grafica de la ventana que muestra los resultados finales.

7. ```cliente.py```: contiene la clase Cliente, encargada de conectarse con el servidor.
8. ```controlador.py```: contiene la clase Controlador que permite conectar al cliente con la interfaz gráfica.
9. ```drag_and_drop.py```: contiene las clases involucradas en el drag and drop.
10. ```parametros.json```: contiene los parametros que son útiles para el cliente.

#### Archivos Python Servidor (carpeta ```server```)

* El módulo ```main.py``` del servidor va acá. También, van los archivos ignorados ```grafo.json```, ```generador_de_cartas.py``` y ```generador_grilla.py```.

1. ```servidor.py```: contiene la clase Servidor que se encarga de aceptar clientes y enviar información.
2. ```logica.py```: contiene la clase Logica que se encarga de procesar información recibida del servidor, y conectarla con el juego (Catan)
3. ```catan.py```: contiene la clase Catan, la cual maneja el juego.
4. ```mapa.py```: contiene la clase Mapa, encargada del grafo del juego. En ella, se instancian Nodos, Caminos y Hexágonos, además de cuardarlos en distintas estruturas.
5. ```jugadores.py```: contiene la clase Jugador. Maneja las acciones propias de cada jugador.
6. ```caminos.py```: contiene la clase Camino (carretera).
7. ```nodo.py```: contiene la clase Nood (choza)
8. ```hexagono.py```: contiene la clase Hexagono.
9. ```parametros.json```: contiene todos los parámetros del juego, y los que necesita el servidor para funcionar.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En general, no realicé supuestos adicionales.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5: este contiene las clases involucradas en el Drag and Drop y contiene los métodos y atributos que permiten esta funcion. Está implementado en el archivo ```drag_and_drop.py```. (Se usan practicamente todas las lineas del archivo).

2. Utilicé códifo de la AF05, algunos métodos iguales por ejemplo para cofidicar y decodificar los mensajes enviados y recibidos. También usé la estructura del código que me permitió modelar mi programa. Algunos métodos son exactamente iguales, otros similares.

3. https://stackoverflow.com/questions/17649875/why-does-random-shuffle-return-none: este contiene codigo que permite desordenar una lista. Lo usé para menzclar la lista de cmainos al alzar y ubicarlos por el servidor en el mapa. Está implementado en el archivo ```catan.py``` en el módulo ```poblar_servidor``` en la linea 55.