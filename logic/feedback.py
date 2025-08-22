import os
import pandas as pd
from config.settings import ADMIN_PASS
import gradio as gr

def enviar_reporte(pregunta, respuesta, comentario):
    archivo = "reportes.csv"
    nuevo_reporte = {
        "Pregunta": pregunta.strip(),
        "Respuesta": respuesta.strip(),
        "Comentario": comentario.strip()
    }

    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        duplicado = ((df["Pregunta"] == nuevo_reporte["Pregunta"]) & (df["Respuesta"] == nuevo_reporte["Respuesta"])).any()
        if duplicado:
            return "⚠️ Ya hemos recibido ese reporte. ¡Gracias por tu interés!"
        df = pd.concat([df, pd.DataFrame([nuevo_reporte])], ignore_index=True)
    else:
        df = pd.DataFrame([nuevo_reporte])

    df.to_csv(archivo, index=False)
    return "✅ ¡Gracias por tu reporte! Se ha registrado exitosamente."

def enviar_y_actualizar(pregunta, respuesta, comentario):
    mensaje = enviar_reporte(pregunta, respuesta, comentario)
    return mensaje, "reportes.csv" if os.path.exists("reportes.csv") else None

def crear_csv_vacio_si_no_existe():
    archivo = "reportes.csv"
    if not os.path.exists(archivo):
        df = pd.DataFrame(columns=["Pregunta", "Respuesta", "Comentario"])
        df.to_csv(archivo, index=False)

def verificar_clave(clave):
    if clave == ADMIN_PASS:
        if os.path.exists("reportes.csv"):
            return gr.update(visible=True), "✅ Acceso a reportes disponible."
        else:
            return gr.update(visible=False), "⚠️ No hay reportes aún."
    else:
        return gr.update(visible=False), "❌ Acceso no disponible por el momento."
