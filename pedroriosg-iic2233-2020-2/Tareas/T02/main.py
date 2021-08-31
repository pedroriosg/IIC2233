import sys
import parametros as p

from PyQt5.QtWidgets import QApplication

from backend_ventana_inicio import BackVentanaInicio
from backend_ventana_juego import BackVentanaJuego
from backend_ventana_rankings import BackVentanaRanking
from backend_ventana_resumen import BackVentanaResumen

from frontend_ventana_inicio import VentanaInicio
from frontend_ventana_juego import VentanaJuego
from frontend_ventana_rankings import VentanaRanking
from frontend_ventana_resumen import VentanaResumen

from backend_flechas import DinamicaFlechas
from backend_flechas import Flecha


def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == '__main__':

    # No modificar
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)

    # Ventana inicio (front-end)
    ventana_inicio = VentanaInicio()
    # Ventana inicio (back-end)
    logica_inicio = BackVentanaInicio()
    # Creamos el registro de archivos
    logica_inicio.crear_txt()
    # Ventana inicio (señales)
    ventana_inicio.senal_verificar_usuario.connect(logica_inicio.verificar_usuario)
    logica_inicio.senal_resultado_verificacion.connect(ventana_inicio.recibir_comparacion)

    # Flechas
    logica_flechas = DinamicaFlechas()

    # Ventana ranking (front-end)
    ventana_ranking = VentanaRanking()
    # Ventana ranking (back-end)
    logica_ranking = BackVentanaRanking()
    # Ventana ranking (señales)
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_volver_a_inicio.connect(ventana_inicio.senal_abrir_ventana_inicio)

    # Ventana juego (front-end)
    ventana_juego = VentanaJuego()
    # Ventana juego (back-end)
    logica_juego = BackVentanaJuego()
    # Ventana juego (señales)
    logica_juego.senal_activa_dinamica_flecha.connect(logica_flechas.inicio_dinamica)
    ventana_inicio.senal_abrir_ventana_juego.connect(ventana_juego.mostrar_y_recibir_usuario)
    ventana_juego.senal_armar_paso.connect(logica_juego.armar_paso)
    logica_juego.senal_aparecer_flecha.connect(ventana_juego.crear_flecha)
    logica_juego.senal_aparecer_flecha.connect(ventana_juego.actualizar_barra)
    ventana_juego.senal_reproducir_cancion.connect(logica_juego.reproducir_cancion)
    ventana_juego.senal_pausa.connect(logica_juego.pausar_paso)
    ventana_juego.senal_pausa.connect(logica_juego.pausar_cancion)
    ventana_juego.senal_pausa.connect(logica_flechas.parar_flechas)
    logica_juego.senal_pausa_tecla.connect(logica_flechas.parar_flechas)
    ventana_juego.senal_agregar_flecha.connect(logica_flechas.correr_flecha)
    ventana_juego.senal_agregar_paso.connect(logica_flechas.agregar_paso)
    # Aca verificamos las teclas apretadas
    ventana_juego.senal_verificar_flecha.connect(logica_juego.verificar_tecla)
    logica_juego.senal_verificar_flecha.connect(logica_flechas.comprobar_flecha)
    # Cheatdocde MON
    ventana_juego.senal_mon.connect(logica_flechas.cheatcode_mon)
    # Cheatcode NIV
    ventana_juego.senal_niv.connect(logica_flechas.cheatcode_niv)
    logica_flechas.senal_cheatcode_niv.connect(logica_juego.pausar_paso)

    logica_flechas.senal_hielo.connect(logica_flechas.activar_hielo)
    logica_flechas.senal_volver_hielo.connect(logica_flechas.vovler_hielo)
    ventana_juego.senal_eviar_tempo.connect(logica_flechas.recibir_tempo)
    logica_flechas.senal_actualizar_etiqueta_combo.connect(ventana_juego.actualizar_combos)
    logica_juego.senal_tecla_invalida.connect(logica_flechas.flecha_invalida)
    logica_flechas.senal_actualizar_aprobacion.connect(ventana_juego.actualizar_aprobacion)
    # Termino de Ronda (ulltima flecha pasa la zona)
    logica_flechas.senal_termino_ronda.connect(logica_juego.parar_cancion_nivel)
    # Setear Label Dinero
    logica_flechas.senal_setear_dinero.connect(ventana_juego.setear_dinero)

    # Ventana Resumen (front - end)
    ventana_resumen = VentanaResumen()
    # Ventana Resumen (back - end)
    logica_resumen = BackVentanaResumen()
    # logica_resumen =
    # Ventana Resumen (señales)
    logica_flechas.senal_termino_ronda.connect(ventana_resumen.senal_abrir_ventana_resumen)
    logica_flechas.senal_eviar_info_ronda.connect(ventana_resumen.recibir_info_y_editar)
    ventana_resumen.senal_verificar_aprobacion.connect(logica_resumen.ver_aprobacion)
    logica_juego.senal_dificultad_nombre.connect(logica_resumen.recibir_dificultad_nombre)
    logica_resumen.senal_activa_boton_siguiente.connect(ventana_resumen.activar_botones)
    
    # Volver a inicio por no pasar nivel
    ventana_resumen.senal_volver_inicio.connect(logica_resumen.volver_inicio)
    ventana_resumen.senal_volver_inicio.connect(ventana_inicio.senal_abrir_ventana_inicio)
    ventana_resumen.senal_volver_inicio.connect(ventana_inicio.limpiar_casilla)
    # Limpair pinguinos
    ventana_resumen.senal_volver_inicio.connect(ventana_juego.limpiar_pista)

    # Seguir jugando despues de continuar una ronda
    ventana_resumen.senal_resetear_combos_barras.connect(logica_flechas.parar_timer_combo)
    ventana_resumen.senal_resetear_combos_barras.connect(ventana_juego.resetear_barras_combos)

    # Escribir en el txt
    logica_resumen.senal_para_agregar_al_txt.connect(logica_inicio.agregar_usuario_txt)

    # Ranking
    ventana_inicio.senal_abrir_ventana_ranking.connect(logica_inicio.enviar_archivo)
    logica_inicio.senal_enviar_lista_a_ordenar.connect(logica_ranking.recibir_y_analizar)
    logica_ranking.senal_enviar_tops.connect(ventana_ranking.actualizar_labels)

    # Limpiar dineros y acumulado
    ventana_inicio.senal_abrir_ventana_juego.connect(logica_flechas.resetear_dinero_y_acumulado)
    ventana_inicio.senal_abrir_ventana_juego.connect(ventana_juego.resetear_dinero)

    # Esconder ventana
    ventana_resumen.senal_volver_inicio.connect(ventana_juego.esconder_ventana)
    logica_flechas.senal_terminar_sin_jugar.connect(ventana_inicio.senal_abrir_ventana_inicio)
    logica_flechas.senal_terminar_sin_jugar.connect(ventana_inicio.limpiar_casilla)

    # SALIR DEL JUEGO
    ventana_juego.senal_salir_juego.connect(logica_flechas.salir_urgente)
    logica_flechas.senal_termino_urgente.connect(logica_resumen.salida_urgente)
    logica_flechas.senal_termino_urgente.connect(logica_juego.pausar_song_y_pasos_para_salir)
    logica_flechas.senal_termino_urgente.connect(ventana_juego.resetear_barras_combos)
    logica_flechas.senal_termino_urgente.connect(ventana_inicio.limpiar_casilla)
    logica_resumen.senal_mostrar_ventana_inicio.connect(ventana_inicio.senal_abrir_ventana_inicio)
    logica_flechas.senal_resetear_barras_combos.connect(ventana_juego.resetear_barras_combos)
    # ________________

    # Pasos pinguinos
    logica_flechas.senal_paso_correcto.connect(ventana_juego.recibir_paso)

    # Cambiar label dienero dps de compra
    ventana_juego.senal_restar_dinero_penguin.connect(logica_flechas.restar_valor_penguin)

    # Cerrar tienda
    ventana_juego.senal_cerrar_tienda.connect(ventana_juego.cerrar_tienda)
    logica_flechas.senal_abrir_tienda.connect(ventana_juego.abrir_tienda)

    # Close Event
    ventana_juego.senal_close_event.connect(logica_flechas.salir_urgente)
    ventana_juego.senal_close_event.connect(ventana_inicio.senal_abrir_ventana_inicio)
    ventana_juego.senal_close_event_sin_comenzar.connect(ventana_inicio.senal_abrir_ventana_inicio)
    ventana_juego.senal_close_event_sin_comenzar.connect(ventana_inicio.limpiar_casilla)

    ventana_inicio.show()
    app.exec()
