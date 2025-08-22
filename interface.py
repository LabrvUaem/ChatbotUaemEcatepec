### 📁 chatbot_app/interface.py

import gradio as gr
from logic.response_engine import respond_letra_por_letra
from logic.response_engine import set_and_respond
from logic.feedback import enviar_y_actualizar, verificar_clave
from logic.chat_manager import chat_manager
from config.settings import ADMIN_PASS


def create_interface():
    with gr.Blocks(theme=gr.themes.Soft(), title="Asistente UAEMex") as app:
        with gr.Column(visible=True) as vista_chatbot:
            gr.Markdown("# 🏛️ Asistente Virtual UAEMex")
            gr.Markdown("### Control Escolar - Campus Ecatepec")

            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=400, type="messages")
                    user_input = gr.Textbox(
                        placeholder="Ej: ¿Qué necesito para cambiar de carrera?",
                        label=""
                    )
                    with gr.Row():
                        submit_btn = gr.Button("Enviar", variant="primary")
                        clear_btn = gr.Button("Limpiar")

                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Preguntas Frecuentes")
                    with gr.Row():
                        btn_becas = gr.Button("Becas")
                        btn_reins = gr.Button("Reinscripción")
                    with gr.Row():
                        btn_pagos = gr.Button("Pagos")
                        btn_titu = gr.Button("Titulación")

                    gr.Markdown("### 🔗 Enlaces Útiles")
                    gr.Markdown("- [SIBECAS](https://sibecas.uaemex.mx/)")
                    gr.Markdown("- [Control Escolar](https://controlescolar.uaemex.mx/)")
                    gr.Markdown("- [Calendario Escolar](http://dep.uaemex.mx/portal/calendario/)")

                    boton_ir_a_reporte = gr.Button("⚠️ ¿El chatbot respondió mal? Envía un reporte")

            gr.Examples(
                examples=[
                    ["¿Cuál es el horario de control escolar?"],
                    ["¿Cómo solicito la beca de Movilidad?"],
                    ["¿Cómo llego a la Uaemex?"],
                    ["¿Cómo puedo solicitar un prestamo de libros?"]
                ],
                inputs=user_input,
                label="💡 Haz clic para probar"
            )

            estado = gr.Label(value="", elem_id="estado")

            submit_btn.click(
                respond_letra_por_letra,
                inputs=[user_input, chatbot],
                outputs=[user_input, chatbot, estado]
            )

            btn_becas.click(
                respond_letra_por_letra,
                inputs=[gr.State("¿Qué tipos de becas existen y sus requisitos?"), chatbot],
                outputs=[user_input, chatbot, estado]
            )
            btn_reins.click(
                respond_letra_por_letra,
                inputs=[gr.State("¿Qué necesito para mi reinscripción?"), chatbot],
                outputs=[user_input, chatbot, estado]
            )
            btn_pagos.click(
                respond_letra_por_letra,
                inputs=[gr.State("¿Dónde puedo hacer pagos escolares?"), chatbot],
                outputs=[user_input, chatbot, estado]
            )
            btn_titu.click(
                respond_letra_por_letra,
                inputs=[gr.State("¿Cuáles son los requisitos para titulación?"), chatbot],
                outputs=[user_input, chatbot, estado]
            )

            clear_btn.click(
                lambda: ([], "", ""),
                None,
                [chatbot, user_input, estado],
                queue=False
            )

        with gr.Column(visible=False) as vista_reporte:
            gr.Markdown("## 🛠️ Ayúdanos a mejorar")
            gr.Markdown("Por favor, cuéntanos qué pregunta hiciste y qué respondió mal el chatbot.")
            gr.Markdown("### 📬 Reportar un error en la respuesta")

            input_pregunta = gr.Textbox(
                label="¿Qué pregunta hiciste?",
                placeholder= "Ej: ¿Qué es lo necesario para la inscripción?")
            input_respuesta = gr.Textbox(
                label="¿Qué respondió el chatbot?",
                placeholder= "Ej: 🎓 Puedes consultarla en Control Escolar o recibirla por correo una vez estés inscrito. La convocatoria suele publicarse entre julio y septiembre del año siguiente al ingreso.",
                lines=3)
            input_comentario = gr.Textbox(
                label="¿Por qué piensas que estuvo mal la respuesta?",
                placeholder= "Ej: ❌ La respuesta no menciona los documentos ni pasos necesarios para inscribirse.\n🤔 Solo dice que se recibe por correo después de estar inscrito, lo cual no tiene sentido si aún no me inscribo. \n✅ Yo esperaba que dijera algo como: “Debes entregar acta de nacimiento, CURP, comprobante de pago, etc.”",
                lines=3)
            btn_enviar_reporte = gr.Button("Enviar reporte")
            label_confirmacion = gr.Label()

            clave_admin = gr.Textbox(label="🔐 Acceder a reportes", type="password")
            btn_verificar_clave = gr.Button("Verificar")
            descarga_csv = gr.File(value="reportes.csv", label="Descargar reportes", interactive=True, visible=False)
            mensaje_clave = gr.Label()

            btn_verificar_clave.click(
                verificar_clave,
                inputs=clave_admin,
                outputs=[descarga_csv, mensaje_clave]
            )

            btn_volver = gr.Button("⬅️ Volver al chatbot")

        def mostrar_reporte():
            return gr.update(visible=False), gr.update(visible=True)

        def volver_a_chatbot():
            return gr.update(visible=True), gr.update(visible=False)

        boton_ir_a_reporte.click(mostrar_reporte, outputs=[vista_chatbot, vista_reporte])
        btn_volver.click(volver_a_chatbot, outputs=[vista_chatbot, vista_reporte])

        btn_enviar_reporte.click(
            enviar_y_actualizar,
            inputs=[input_pregunta, input_respuesta, input_comentario],
            outputs=[label_confirmacion, descarga_csv]
        )

    return app
