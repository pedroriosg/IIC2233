# Tarea 02: DCCumbia :school_satchel:

## Consideraciones generales :octocat:

* En primer lugar, quería pedir disculpas ya que el código está un poco desordenado. La verdad es que no pude comenzar la tarea a la fecha que me hubiese gustado, y eso me llevo a programar apurado, contra el tiempo, y de manera desordenada. Sin embargo, trataré de ser lo más explicativo posible en este ```README```.

*  En segundo lugar, al momento de subir la tarea por última vez al repositorio, no me di cuenta de que tenía las rutas de las canciones (las dos) distintas a las correctas, ya que probé mo código con canciones que yo descargué. Esto lo solucioné realizando un nuevo ```push```aproximadamente 40 minutos después de las 20:00 hrs. El cambio se produjo en el archivo ```backend_ventana_juego.py```en el método ```reproducir_cancion```en las líneas ```75```y ```77```.

* En el archivo ```parametros.py```me faltaron algunas parametrizaciones. En primer lugar, las rutas. Las rutas de las canciones no están parametrizadas, así como tampoco la de las imágenes de los pingüirines (esto ya que uso rutas usando ```f"{string}"```). Tampoco está parametrizado el ```ALTO_CAPTURA``` ya que este está fijo del ```QtDesigner```. Por último, la cantidad de usuarios que se muestran en el ranking no está parametrizada, ya que es fija, esto lo hice porque tengo ```QLabels``` predeterminados en el ```QtDesigner```.

* En general el juego funciona de manera correcta, tengo problemas con el botón de pausa, que será explicado más abajo. También, es condición para que el puntaje quede resgistrado que se comienze la partida. Producto de programar apurado no pude lograr en ocasiones una buena separacion ```frontend - backend```. 

* Los botones se desactivan según la fase en que se encuentre el jugador. Por ejemplo, no se puede poner pausa si no se ha comenzado la partida, y al momento de comenzar, se desactiva la tienda, y los botones para seleccionar las canciones y el nivel de dificultad, así como también el boton para comenzar la partida. Al terminar la ronda, se vuelven a activar.

* En relación al uso de PEP8, no tuve problemas, sin embargo no pude comentar el código como me hubiese gustado.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Ventama de Inicio:**

    * La ventana de inicio se visualiza correctamente. Los elementos no se superponen entre sí: COMPLETO
    * Se puede crear una partida nueva, verificando que el nombre sea alfanumérico. De lo contrario se señala que no es correcto: COMPLETO. En ```frontend_ventana_inicio.py``` al hacer click en el botón ```Ver Ranking```, el programa conecta con el método ```verificar_usuario```, el cual envía el texto de la casilla a traves de señales (```senal_verificar_usuario```) a el archivo ```backend_ventana_inicio.py``` al método ```verificar_usuario``` (linea ```18```) en donde se revisa si es alfanumérico. Luego, se envía una señal ```senal_resultado_verificacion``` con el resultado de la comprobación a ```frontend_ventana_inicio.py``` al método ```recibir_comparacion``` (linea ```30```) en donde, si no se cumple la condición, se señala el error mediante una ```QMessageBox```(entre las lineas ```35```y ```39```).

* **Ventana de Ranking:**

    * La ventana de ranking se visualiza correctamente. Los elementos no se superponen entre sí: COMPLETO
    * Se muestra la cantidad correcta de puntajes ordenados de manera decreciente: COMPLETO. La cantidad correcta de puntajes es una cantidad fija (5 como máximo), ya que no está parametrizado. El ordenamiento se realiza en el archivo ```backend_ventana_rankings.py``` en el método ```recibir_y_analizar``` (linea ```16```), en donde se ordena de manera decreciente para finalemente enviar la tupla con los puntajes y usuario a ```frontend_ventana_rankings.py```, en donde, el el método ```actualizar_labels``` se actualizan las etiquetas de la interfaz.

* **Ventana de Juego:**

    * **Generales:**

        * Se diferencian correctamente las cuatro áreas del juego. Los elementos no se superponen entre sí: COMPLETO
        * Se visualizan correctamente las estadísticas del juego. Los elementos no se superponen entre sí: COMPLETO
        * Se muestran la tienda con pingüirines que se pueden comprar y su precio. Los elementos no se superponen entre sí: COMPLETO
        * El boton Salir cierra la ventana y vuelve a la ventana de inicio: COMPLETO. Al hacer click en el boton ```Salir```, el programa conecta con el método ```salir_juego``` (archivo ```frontend_ventana_juego.py``` (linea ```120```)) el cual, no cierra la ventana, sino que la oculta con el método ```.hide()``` (de todas maneras, al volver a la ventana de Inicio se resetean todos los valores). Luego, se pueden emitir dos señales, la señal ```senal_salir_juego``` o ```senal_close_event_sin_comenzar```. La ```senal_close_event_sin_comenzar``` conecta directamente con la señal ```senal_abrir_ventana_inicio``` del archivo ```frontend_ventana_inicio.py```, en donde se abre la ventana señalada. Esta señal está conectada en el archivo ```main.py``` en la linea ```152```. Por otro lado, la ```senal_salir_juego``` conecta con el método ```salir_urgente```del archivo ```backend_flechas.py``` en donde, dependiento de cada caso, se emiten distintas señales (```senal_termino_urgente``` o ```senal_terminar_sin_jugar```) las cuales conectan, en el archivo ```main.py```en las lineas ```126```y ```135``` con la señal ```senal_abrir_ventana_inicio``` del archivo ```frontend_ventana_inicio.py```.

    * **Fase Pre - Ronda:**

        * Al iniciar una partida, se debe seleccionar un pingüirin inicial,una cancion y la dificultad antes de permitir pasar a la fase de ronda: COMPLETO. Se debe si o si elegir un pingüirin incial, si se clickea ```Comenzar Partida```se inicia el juego con las canciones y dificultad predeterminadas (```Cancion 1``` y ```Principiante```).
        * Se descuenta el dinero de comprar un pingüirín si se puede comprar, actualizando la información correspondiente: COMPLETO. Esto se realiza en el archivo ```backend_flechas``` en el método ```restar_valor_penguin```, el cual ejecuta el metodo ```setear_dinero``` el cual emite una señal que conecta (```main.py``` linea ```87```) con el archivo ```frontend_ventana_juego.py```  y el método ```setear_dinero```(linea ```210```)
        * Se pueden comprar pingüirines de forma correcta lo hace con un correcto uso de señales y drag and drop: COMPLETO. Al momento de hacer el ```dropEvent``` se revisa si el dinero disponible es mayor al del pingüirin (archivo ```drag_and_drop``` linea ```31```), si es mayor, se permite realizar el evento. Cada QLabel que almacena un pingüirin tiene un atributo dinero, que se actualiza constantemente debido a un QTimer que se incia en el archivo ```frontend_ventaja_juego.py``` en el método ```crear_label_pingüinos``` en la linea ```230``` que conecta con la funcion ```comprar_pinguino``` del mismo archivo, esto permite comprar unica y exclusivamente cuando se tiene el dinero. Esta última funcion llama a ```cambiar_dinero``` (presente en el mismo archivo), que emite la ```senal_restar_valor_penguin```, la cual conecta con el archivo ```backend_flechas``` y el método ```restar_valor_penguin```, que realiza lo descrito en el punto anterior.
        * Los pingüirines no se sobreponen ni se pueden colocar en posiciones inválidas: COMPLETO. (se genero para mayor simplicidad una pista con QLabels cuadrados).
        * Se puede seleccionar una canción y un nivel de dificultad. Lo hace con un correcto uso de señales: COMPLETO. Al momento de comenzar la partida (```main.py```, método ```comenzar_partida```) guarda la dificultad y el numero de la cancion en variables. La dificultad luego permite generar pasos y setear de manera correcta la barra de progreso (se emiten señales para eso). Por otro lado, con el indice de la cancion se emite la señal para luego reproducirla (conecta con ```backend_ventana_juego.py``` metodo ```reproducir_cancion```)
    
    * **Fase Ronda:**

        * Se aprecia el cambio en la duración de la ronda, generación de pasos y combinaciones de flechas de acuerdo a la dificultad elegida: COMPLETO
        * Se reproduce la canción elegida. Se implementa mediante PyQt5: COMPLETO
        * Se marca correctamente la zona de captura según las teclas presionadas: COMPLETO
        * Las estadísticas se actualizan a medida que progresa el juego: COMPLETO. Los combos se actualizan constantemente al igual que las barras de progreso, esto se realiza en el archivo ```frontend_ventana_juego``` en los metodos ```actualizar_barras``` y ```actualizar_combos```. Estos metodos se llaman cuando se conectan distintas señales. Esto se puede ver en el archivo ```main.py``` en las lineas ```61``` y ```81```. (estas señales se emiten constantemente, hay QTimers para ello)
        * Se calcula correctamente la aprobación del público: COMPLETO. Se calcula en el archivo ```backend_flechas.py``` en el método ```aprobacion``` en la linea ```259```.
        * Se lleva correctamente el conteo del combo: COMPLETO
        * La ronda termina una vez transcurre el tiempo dado por la dificultad: COMPLETO. Se terminan de generar flechas cuando acaba un QTimer creado en el archivo ```backend_ventana_juego.py``` en la línea ```34```. Al momento de reproducir la cancion, se genera un nuevo QTimer (linea ```66``` del mismo archivo), que segun la dificultad del nivel, para el QTimer que genera flechas. Sin embargo, la cancion no se acaba hasta que la ultima flecha desaparece de la zona de ritmo, luego de eso se muestra la ventana de resumen (ahí se termina la ronda). Esto se ve reflejado en el archivo ```backend_flechas.py``` en el método ```revisar_termino``` linea ```265```.
    
    * **Fase Post - Ronda:**

        * Se visualiza una ventana con los resultados y un botón para pasar a la siguiente. Los elementos no se superponen entre sí: COMPLETO
        * Las estadisticas post-ronda son correctas y reflejan el resultado de la ronda: COMPLETO
        * Se calcula correctamente el puntaje de la ronda: COMPLETO. El puntaje de la ronda se calcula en el archivo ```backend_flechas``` en el método ```puntaje_final``` (linea ```188```)
        * Si la aprobación llega a ser menor al nivel pedido en la dificultad, el juego se termina y se incluye la opcion para volver a la ventana inicial: COMPLETO. En el archivo ```backend_ventana_resumen.py``` en el metodo ```ver_aprobacion``` se verifica la aprobacion y dependiendo de eso, se envia la ```senal_activa_boton_siguiente``` la cual conecta con el archivo ```frontend_ventana_resumen.py``` y el metodo activar botones, que determinan QLabels y habilitan botones para continuar jugando o volver al inicio. Luego, dependiendo del click del boton, se sigue el juego.

* **Mecánicas:**:

    * **Pingüirin:**

        * Se muestra consistencia entre las teclas apretadas y el movimiento del pingüirin. Lo hace con un correcto uso de señales: COMPLETO. Luego de ejecutar cada paso correctamente, se emite una señal. Esto pasa en el archivo ```backend_flechas.py``` en el método ```kombo```. Acá se emite la ```senal_paso_correcto``` que envía el paso. Esta señal conecta con el método del archivo ```frontend_ventana_juego``` llamado ```recibir_paso``` (esto se puede ver en la linea ```140``` del ```main.py```). Al recibir el paso, se le indica a todos los pingüirines que se muevan, y vuelvan a su posicion original. Esto se hace en el método ```moverse```de la clase ```Espacio``` en el archivo ```drag_and_drop.py```
        * Todos los pingüinos bailan simultaneamente, siguiendo los mismos pasos: COMPLETO
        * Al cambiar de un paso a otro, se pasa por la posición neutral: COMPLETO

    * **Flechas:**

        * El movimiento de las flechas es fluido y cambia de posición correctamente. Lo hace con un correcto uso de señales y threading: COMPLETO. El moviento de las flechas se concreta en el archivo ```backend_flechas.py``` en la clas ```Flecha``` , método ```movimiento``` linea ```50```. El metodo se ejecuta constantemente por un QTimer.
        * Implementa correctamente la flecha normal: COMPLETO (Flecha Verde)
        * Implementa correctamente la flecha x2: COMPLETO (Flecha Roja)
        * Implementa correctamente la flecha dorada: COMPLETO (Flecha Dorada)
        * Implementa correctamente la flecha hielo: COMPLETO (Flecha Morada)
        * Flechas desaparecen al ser capturadas: COMPLETO
        * Las flechas no capturadas siguen bajando al llegar al final de la "zona de ritmo: COMPLETO
        * Identifica correctamente si un paso normal es correcto o no: COMPLETO. Todos los pasos se verifican si son correctos en el archivo ```backend_flechas.py``` en el metodo ```kombo```. Luego, si el paso es correcto, se envian señales y se actualizan distintos atributos.
        * Identifica correctamente si un paso combinado es correcto o no: COMPLETO. Todos los pasos se verifican si son correctos en el archivo ```backend_flechas.py``` en el metodo ```kombo```. Luego, si el paso es correcto, se envian señales y se actualizan distintos atributos.

* **Funcionalidades Extra:**

    * **Pausa:**

        * Esta implementado el botón Pausa y la letra P, al seleccionarlo se detiene la música y todas las animaciones. Además se deshabilita la interacción del teclado de flechas con el juego: SEMI - COMPLETO. El boton de pausa funciona, al igual que apretar la tecla P. Se detiene la musica y todas las interacciones, pero no se deshabilita la interaccion del teclado de flechas con el juego. Además, no pude hacer que el programa genere flechas por la misma cantidad de tiempo que estuvo en pausa, pasado el tiempo "regular" del nivel. Todo esto sucede al hacer click en el boton ```Pausa``` o apretar la letra ```p``` del teclado. Si se apreta el boton de Pausa, en el archivo ```frontend_ventana_juego.py``` en el método ```pasua``` se emite una señal que coencta, en el ```main.py``` con metodos para pausar canciones, generacion de pasos y movimiento de flechas (lineas ```63``` a ```65```). Con respecto a la letra ```p```, al ser un ```keyPressEvent```, se valida en el archivo ```backend_ventana_juego.py``` y si es una ```p``` se ejecutan las mismas funciones que con el boton ```Pausar```
    
    * **M + O + N:**

        * Al escribir esta combinación de letras en orden o al mismo tiempo, aumenta el dinero del jugador: COMPLETO. El dinero se aumenta al final de la ronda. Se verifica si está la secuencia M + O + N, en el archivo ```frontend_ventana_juego.py``` en el metodo ```keyPressEvent``` (linea (```155```)) y se emite una señal, la cual conecta en ```main.py``` linea ```73``` con el archivo ```backend_flechas``` y el método ```cheatcode_mon``` el cual aumenta el dinero.
    
    * **N + I + V:**

        * Al escribir esta combinación de letras en orden o al mismo tiempo, termina la ronda, calculando correctamente lo realizado al momento. No se puede usar en la fase de pre-ronda: SEMI - COMPLETO. Se verifica si está la secuencia N + I + V, en el archivo ```frontend_ventana_juego.py``` en el metodo ```keyPressEvent``` (linea (```158```)) y se emite una señal, la cual conecta en ```main.py``` linea ```73``` con el archivo ```backend_flechas``` y el método ```cheatcode_niv``` el cual termina el nivel. Sin embargo, el uso no está bloqueado en la fase pre - ronda.

* **General:**

    * **Modularizacion:**

        * Adecuada separación entre back-end y front-end: Los modulos están bien divididos, sin embargo no pude generar un bajo acoplamiento y una alta cohesión como me hubiese gustado.
    
    * **Modelación:**

        * Bajo acomplamiento y alta cohesión del programa: El programa tiene bajo acomplamiento y alta cohesión solo con algunas funcionalidades, sin embargo no en su totalidad. A veces es dificil de seguirle la pista. Esto me sucedió ya que programé muy contra el tiempo.

    * **Archivos:**

        * Trabaja correctamente con todos los archivos  entregados: COMPLETO. Se utilizan rutas relativas para acceder a la informacion de las carpetas entregadas. Se usan rutas para las canciones en el archivo ```backend_ventana_juego.py``` en el método ```reproducir_cancion``` en las lineas ```75``` y ```77```. Se usan rutas para las flechas en el archivo ```frontend_ventana_juego.py``` en el método ```crear_flechas``` en la linea ```82```. Se usan rutas para los movimientos de los pingüirines en el archivo ```drag_and_drop``` en el método ```moverse``` entre las lineas ```51``` y ```79```.


    * **Parametros.py:**

        * Utiliza e importa correctamente parametros.py: COMPLETO. Se importa al inicio de cada documento ```.py```.
        * Contiene todos los parámetros pedidos en el enunciado: INCOMPLETO. El archivo no contiene parametrizadas las rutas de las imagenes y canciones. Además le falta el parametro ```ALTO_CAPTURA``` y el que determina la cantidad de usuarios que se muestran en la ventana de ranking.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Los archivos necesarios para que el código funcione son los indicados en la sección **Librerias Propias** (junto con el ```main.py```)

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```uic```
2. ```PyQt5.QtWidgets```: ```QApplication```, ```QLabel```, ```QWidget```, ```QMessageBox```
3. ```PyQt5.QtGui```: ```QDrag```, ```QPixmap```, ```QPainter```, ```QCursor```, ```QImage```
4. ```PyQt5.QtCore```: ```QMimeData```, ```Qt```, ```QTimer```, ```QThread```, ```QObject```, ```pyqtSignal```, ```QRect```, ```QUrl```
5. ```PyQt5.QtMultimedia```: ```QSound```
6. ```sys```
7. ```os```
8. ```time```: ```sleep```, ```time```
9. ```random```: ```randint```
10. ```math```: ```floor```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### QtDesigner

1. ```designer_inicio.ui```: Contiene elementos gráficos de la ventan de inicio.
2. ```designer_juego.ui```: Contiene elementos gráficos de la ventan de juego.
3. ```designer_rankings.ui```: Contiene elementos gráficos de la ventan de rankings.
4. ```designer_resumen.ui```: Contiene elementos gráficos de la ventan de resumen.

#### Archivos Python

1. ```frontend_ventana_inicio.py```: maneja la grafica de la ventana de inicio.
2. ```frontend_ventana_juego.py```: maneja la grafica de la ventana de juego.
3.  ```frontend_ventana_rankings.py```: maneja la grafica de la ventana de rankings.
4. ```frontend_ventana_resumen.py```: maneja la grafica de la ventana de resumen.
5. ```backend_ventana_inicio.py```: contiene las funciones que determinan que se muestra en la ventana de inicio.
6. ```backend_ventana_juego.py```: contiene las funciones que determinan que se muestra en la ventana de juego.
7. ```backend_ventana_rankings.py```: contiene las funciones que determinan que se muestra en la ventana de ranking.
8. ```backend_ventana_resumen.py```: contiene las funciones que determinan que se muestra en la ventana de resumen.
9. ```backend_flechas.py```: contiene la dinamica de las flechas, movimiento, comrpbacion de pasos, etc.
10. ```parametros.py```: contiene los parametros.
11. ```drag_and_drop.py```: contiene las clases del drag and drop.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En general, no realicé supuestos adicionales.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5: este contiene las clases involucradas en el Drag and Drop y contiene los métodos y atributos que permiten esta funcion. Está implementado en el archivo ```drag_and_drop.py```. (Se usan practicamente todas las lineas del archivo)
2. https://www.youtube.com/watch?v=GkgMTyiLtWk&t=156s: este me ayuda a implementar el ```QMessageBox```, está implementado en el archivo ```frontend_ventana_inicio.py``` en el método ```recibir_comparacion``` entre las lineas ```35```y ```39```. También en el archivo ```frontend_ventana_juego.py``` en el módulo ```comenzar_partida``` entre las lineas ```115```y ```118```.
