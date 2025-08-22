import time
from logic.chat_manager import chat_manager
from model.loader import pipe
from config.instructions import SYSTEM_INSTRUCTIONS
from config.knowledge import UAEMEX_KNOWLEDGE
from logic.utils import normalize_text


def generate_response(user_query):
    if not user_query.strip():
        return "🎓 Por favor, escribe tu pregunta sobre trámites UAEMex."

    entrada_simple = [
        "hola", "buenas", "saludos", "hey", "holi", "qué tal",
        "holaa", "holaaa", "hey!", "buenas días", "buenos días",
        "buenas tardes", "buenos tardes", "buenas noches", "buenos noches",
        "que tal", "qué onda", "que onda", "qué hubo", "que hubo",
        "qué pasa", "que pasa", "saludos cordiales",
        "buen día", "buen día a todos", "buenos días a todos",
        "buenas tardes a todos", "buenas noches a todos",
        "holis", "holla", "hooola", "buen dia", "buenas!", "heyyy"
    ]

    user_query_normalized = normalize_text(user_query.strip())

    if user_query_normalized in [normalize_text(x) for x in entrada_simple]:
        return "🎓 ¡Hola! Por favor, hazme una pregunta específica sobre trámites académicos para poder ayudarte mejor."

    unrelated_terms = ["futbol", "pelicula", "musica", "redes sociales"]
    if any(term in user_query_normalized for term in unrelated_terms):
        return "⚠️ Solo respondo preguntas sobre trámites académicos."

    for main_topic, data in UAEMEX_KNOWLEDGE.items():
        if "subtypes" in data:
            for subtype, response in data["subtypes"].items():
                if normalize_text(subtype) in user_query_normalized:
                    return response

    for topic, data in UAEMEX_KNOWLEDGE.items():
        if any(normalize_text(keyword) in user_query_normalized for keyword in data["keywords"]):
            return data["response"]

    context_text = ""
    for msg in chat_manager.get_context():
        prefix = "Usuario: " if msg["role"] == "user" else "Asistente: "
        context_text += f"{prefix}{msg['content']}\n"

    prompt = (
        f"{SYSTEM_INSTRUCTIONS}\n"
        f"{context_text}"
        f"Usuario: {user_query}\n"
        f"Asistente: "
    )

    try:
        output = pipe(
            prompt,
            max_new_tokens=150,
            temperature=0.9,
            top_p=0.8,
            repetition_penalty=1.2,
            do_sample=True
        )
        response = output[0]["generated_text"].strip()

        if "Usuario:" in response:
            response = response.split("Usuario:")[0].strip()
        if "Asistente:" in response:
            response = response.split("Asistente:")[-1].strip()

        if not response.startswith("🎓"):
            response = f"🎓 {response}"

        if len(response) > 600 or any(
            phrase in response.lower() for phrase in ["testigo", "celebraron", "fotos", "abrazos"]
        ):
            return (
                "🎓 Lo siento, no puedo responder esa pregunta con información confiable. "
                "Por favor intenta con otra consulta o revisa la página oficial."
            )

        if "$" in response and "pago" not in user_query_normalized and "costo" not in user_query_normalized:
            response += "\n\nℹ️ Para información financiera exacta, consulta en Control Escolar"

        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        return "🎓 Ocurrió un error al generar la respuesta. Intenta de nuevo."


def respond_letra_por_letra(message, chat_history):
    chat_manager.add_message("user", message)
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": message})

    chat_history.append({"role": "assistant", "content": "Thinking..."})
    yield "", chat_history, ""

    time.sleep(4)

    respuesta = generate_response(message)
    chat_manager.add_message("assistant", respuesta)

    texto_actual = ""
    for letra in respuesta:
        texto_actual += letra
        chat_history[-1]["content"] = texto_actual
        yield "", chat_history, ""
        time.sleep(0.01)

    yield "", chat_history, ""


def set_and_respond(question, chat_history):
    chat_manager.add_message("user", question)
    bot_response = generate_response(question)
    chat_manager.add_message("assistant", bot_response)
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": bot_response})
    return "", chat_history, ""