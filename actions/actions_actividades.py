
# This is a simple example for a custom action which utters "Hello World!"

import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from rasa_sdk.events import SlotSet


#tipo de actividades que se muestran 
class ActionFiltrarOpciones(Action):
    def name(self) -> Text:
        return "action_filtrar_opciones"

    def run(self, dispatcher, tracker, domain):
        # mostrar_todas_str = tracker.get_slot("slot_actividades_all")
        # mostrar_todas = mostrar_todas_str == "true"
        varEmocion = tracker.get_slot("slot_tipo_emocion")
        mostrar_todas = False
        if mostrar_todas:
            dispatcher.utter_message(response="utter_menu_mostrarAll")
        else:
            if varEmocion == "negativo":
                dispatcher.utter_message(response="utter_menu_list_actividadesN")
            elif varEmocion == "positivo":
                dispatcher.utter_message(response="utter_menu_list_actividadesP")
            elif varEmocion == "neutro":
                dispatcher.utter_message(response="utter_menu_list_actividadesNE")
            else:
                dispatcher.utter_message(text="No se pudo identificar la emoción actual. Por favor, intenta de nuevo.")

        # Resetear el slot después de mostrar las actividades
        return []
    

# class ActionEjecutarOpcion(Action):
#     def name(self) -> Text:
#         return "custom_action_ejecutar_opcion"

#     def run(self, dispatcher: CollectingDispatcher, 
#             tracker: Tracker, 
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # 1. Obtener la emoción actual del slot
#         varEmocion = tracker.get_slot("slot_tipo_emocion")
        
#         # 2. Extraer el número seleccionado (de entidades o botones)
#         varNumero = next(tracker.get_latest_entity_values("ent_numActividad"), None)
#         print(f"NUMEROO: {varNumero}")
        
#         # 3. Mapeo de opciones por emoción
#         opciones = {
#             "negativo": {
#                 "1": "utter_detalle_respiracion",
#                 "2": "utter_detalle_escritura",
#                 "3": "utter_detalle_audio",
#                 "4": "utter_detalle_estiramientos"
#             },
#             "positivo": {
#                 "1": "utter_detalle_baile",
#                 "2": "utter_detalle_gratitud",
#                 "3": "utter_detalle_proyecto",
#                 "4": "utter_detalle_compartir"
#             },
#             "neutro": {
#                 "1": "utter_detalle_meditacion",
#                 "2": "utter_detalle_organizar",
#                 "3": "utter_detalle_leer",
#                 "4": "utter_detalle_hidratacion"
#             }
#         }

#         # 4. Validación y respuesta
#         if not varEmocion or not varNumero:
#             dispatcher.utter_message(text="No detecté tu selección. Por favor elige una opción válida.")
#         elif varEmocion in opciones and varNumero in opciones[varEmocion]:
#             dispatcher.utter_message(response=opciones[varEmocion][varNumero])
#         else:
#             dispatcher.utter_message(text=f"⚠️ La opción {varNumero} no está disponible para emociones {varEmocion}.")

#         return []
    

class ActionEjecutarOpcion(Action):
    def name(self) -> Text:
        return "custom_action_ejecutar_opcion"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # # ✅ VERIFICAR SI ESTAMOS EN FEEDBACK - ESTA ES LA SOLUCIÓN
        # feedback_pendiente = tracker.get_slot("slot_feedback_pendiente")
        # encuesta_completada = tracker.get_slot("slot_encuesta_completada")
        
        # # Si estamos en medio de feedback, NO procesar opciones
        # if feedback_pendiente or encuesta_completada:
        #     return []  # ← Retornar vacío, no hacer nada

        # 1. Obtener la emoción actual del slot
        varEmocion = tracker.get_slot("slot_tipo_emocion")
        
        # 2. Extraer el número seleccionado (de entidades o botones)
        varNumero = next(tracker.get_latest_entity_values("ent_numActividad"), None)
        print(f"NUMEROO: {varNumero}")
        
        # 3. Mapeo de opciones por emoción con acción y actividad
        opciones = {
            "negativo": {
                "1": {"accion": "utter_detalle_respiracion", "actividad": "respiracion"},
                "2": {"accion": "utter_detalle_escritura", "actividad": "escritura"},
                "3": {"accion": "utter_detalle_audio", "actividad": "audio"},
                "4": {"accion": "utter_detalle_estiramientos", "actividad": "estiramientos"}
            },
            "positivo": {
                "1": {"accion": "utter_detalle_baile", "actividad": "baile"},
                "2": {"accion": "utter_detalle_gratitud", "actividad": "gratitud"},
                "3": {"accion": "utter_detalle_proyecto", "actividad": "proyecto"},
                "4": {"accion": "utter_detalle_compartir", "actividad": "compartir"}
            },
            "neutro": {
                "1": {"accion": "utter_detalle_meditacion", "actividad": "meditacion"},
                "2": {"accion": "utter_detalle_organizar", "actividad": "organizar"},
                "3": {"accion": "utter_detalle_leer", "actividad": "leer"},
                "4": {"accion": "utter_detalle_hidratacion", "actividad": "hidratacion"}
            }
        }

        # 4. Validación y respuesta
        if not varEmocion or not varNumero:
            dispatcher.utter_message(text="No detecté tu selección. Por favor elige una opción válida.")
            return []
        
        if varEmocion in opciones and varNumero in opciones[varEmocion]:
            seleccion = opciones[varEmocion][varNumero]
            dispatcher.utter_message(response=seleccion["accion"])
            # Devolver SlotSet para guardar la actividad elegida
            return [SlotSet("slot_ejercicio_actual", seleccion["actividad"])]
        
        dispatcher.utter_message(text=f"⚠️ La opción {varNumero} no está disponible para emociones {varEmocion}.")
        return []


# class ActionOfrecerActividad(Action):
#     def name(self) -> Text:
#         return "action_ofrecer_actividad"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         varTipoEmocion = tracker.get_slot("slot_tipo_emocion")
        
#         # Definir los mensajes según la emoción
        
#         mensajes = {
#             "negativo": "😔 Entiendo que estás teniendo un momento difícil, algo común cuando nos enfrentamos a situaciones sociales. ¿Te gustaría probar una **técnica rápida** para manejar estas emociones?",
#             "positivo": "😊 ¡Genial que te sientas así! Es un buen momento para **practicar alguna habilidad social** y seguir mejorando. ¿Te interesa?",
#             "neutro": "😐 Los días neutrales son ideales para **prepararnos para futuras conversaciones**. ¿Quieres explorar algún ejercicio?"
#         }
        
#         # Obtener el mensaje o usar uno por defecto
#         mensaje = mensajes.get(varTipoEmocion, "No detecté tu selección. Por favor elige una opción válida.")
        
#         # Enviar mensaje con botones
#         dispatcher.utter_message(
#             text=mensaje,
#             # buttons=[
#             #     {"title": "✅ Sí, muéstrame actividades", "payload": "/int_si_actividades"},
#             #     {"title": "❌ No, ahora no", "payload": "/int_no_actividades"}
#             # ]
#             buttons=[
#                 {
#                     "title": "🧠 Sí, quiero una actividad", 
#                     "payload": "/int_si_actividades"
#                 },
#                 {
#                     "title": "🔄 Tal vez después", 
#                     "payload": "/int_no_actividades"
#                 }
#             ]
#         )
        
#         return []
    
    
class ActionOfrecerActividad(Action):
    def name(self) -> Text:
        return "action_ofrecer_actividad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        varTipoEmocion = tracker.get_slot("slot_tipo_emocion")
        
        # Definir los mensajes según la emoción
        mensajes = {
            "negativo": "😔 Entiendo que estás teniendo un momento difícil, algo común cuando nos enfrentamos a situaciones sociales. ¿Te gustaría probar una **técnica rápida** para manejar estas emociones?",
            "positivo": "😊 ¡Genial que te sientas así! Es un buen momento para **practicar alguna habilidad social** y seguir mejorando. ¿Te interesa?",
            "neutro": "😐 Los días neutrales son ideales para **prepararnos para futuras conversaciones**. ¿Quieres explorar algún ejercicio?"
        }
        
        # Obtener el mensaje o usar uno por defecto
        mensaje_texto = mensajes.get(varTipoEmocion, "No detecté tu selección. Por favor elige una opción válida.")
        
        # Botones inline - CADA BOTÓN EN SU PROPIA FILA
        botones = [
            [{"text": "🧠 Sí, quiero probar una actividad", "callback_data": "/int_si_actividades"}],
            [{"text": "🔄 Tal vez después", "callback_data": "/int_no_actividades"}]
        ]

        mensaje = {
            "text": mensaje_texto,
            "reply_markup": {"inline_keyboard": botones}
        }

        dispatcher.utter_message(json_message=mensaje)
        return []    
    
    
#Mostrar todas las actividades 
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionEjecutarCualquiera(Action):
    def name(self) -> Text:
        return "custom_action_ejecutar_cualquiera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Obtener número seleccionado desde la entidad
        varNumero = next(tracker.get_latest_entity_values("ent_numActividad"), None)
        print(f"[DEBUG] Actividad seleccionada: {varNumero}")

        # 2. Mapeo de las 12 actividades (sin importar emoción)
        actividades = {
            "1":  {"accion": "utter_detalle_respiracion",    "actividad": "respiracion"},
            "2":  {"accion": "utter_detalle_escritura",      "actividad": "escritura"},
            "3":  {"accion": "utter_detalle_audio",          "actividad": "audio"},
            "4":  {"accion": "utter_detalle_estiramientos",  "actividad": "estiramientos"},
            "5":  {"accion": "utter_detalle_baile",          "actividad": "baile"},
            "6":  {"accion": "utter_detalle_gratitud",       "actividad": "gratitud"},
            "7":  {"accion": "utter_detalle_proyecto",       "actividad": "proyecto"},
            "8":  {"accion": "utter_detalle_compartir",      "actividad": "compartir"},
            "9":  {"accion": "utter_detalle_meditacion",     "actividad": "meditacion"},
            "10": {"accion": "utter_detalle_organizar",      "actividad": "organizar"},
            "11": {"accion": "utter_detalle_leer",           "actividad": "leer"},
            "12": {"accion": "utter_detalle_hidratacion",    "actividad": "hidratacion"},
        }

        # 3. Verificar si el número existe en el diccionario
        if varNumero and varNumero in actividades:
            seleccion = actividades[varNumero]
            dispatcher.utter_message(response=seleccion["accion"])
            return [SlotSet("slot_ejercicio_actual", seleccion["actividad"])]
            
        else:
            dispatcher.utter_message(text="Lo siento, no reconozco esa actividad. Elige un número del 1 al 12.")
        
        # 4. (Opcional) limpiar slot si lo usas
        #return [SlotSet("slot_opcion_actividad", None)]
        return []



class ActionMostrarMenuAll(Action):
    def name(self) -> Text:
        return "action_mostrar_menu_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Recuperar el nombre del usuario desde el slot
        # varNombre = tracker.get_slot("slot_name")
        # if not varNombre:
        #     varNombre = "usuario"  # valor por defecto si el slot está vacío
            
        actividades = [
            "1️⃣ 🌬️ Respira",
            "2️⃣ ✍️ Escribe",
            "3️⃣ 🎧 Audio",
            "4️⃣ 🤸 Estira",
            "5️⃣ 😊 Comparte",
            "6️⃣ 💃 Bailar",
            "7️⃣ 🎨 Creativo",
            "8️⃣ 📝 Gratitud",
            "9️⃣ 🧘 Medita",
            "🔟 🧹 Ordena",
            "11️⃣ 📖 Leer",
            "12️⃣ 💧 Hidratación"
        ]

        # Convertir actividades en payload para Rasa
        botones = [
            [{"text": act, "callback_data": f'/int_sel_actividadAll{{"ent_numActividad":"{i+1}"}}'} 
             for i, act in enumerate(actividades)][j:j+2] 
            for j in range(0, len(actividades), 2)
        ]

        mensaje = {
            "text": "Elige la que mas te llame la atención:",
            "reply_markup": {"inline_keyboard": botones}
        }

        dispatcher.utter_message(json_message=mensaje)
        return []



class ActionMenuSelActividad(Action):
    def name(self) -> Text:
        return "action_menu_sel_actividad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        botones = [
            [
                {"text": "🔴 Opción 1", "callback_data": '/int_sel_actividad{"ent_numActividad":"1"}'},
                {"text": "🟡 Opción 2", "callback_data": '/int_sel_actividad{"ent_numActividad":"2"}'},
                {"text": "🟢 Opción 3", "callback_data": '/int_sel_actividad{"ent_numActividad":"3"}'}
            ],
            [
                {"text": "⭐ Opción 4", "callback_data": '/int_sel_actividad{"ent_numActividad":"4"}'},
                {"text": "📋 Ver todas", "callback_data": '/int_actividades_mostrarAll{"ent_actividades_all":"false"}'}
            ]
        ]

        mensaje = {
            "text": "Elige el numero de actividad que te interesa:",
            "reply_markup": {"inline_keyboard": botones}
        }

        dispatcher.utter_message(json_message=mensaje)
        return []



class ActionMenuNoProfundizarActividades(Action):
    def name(self) -> Text:
        return "action_menu_no_profundizar_actividades"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        botones = [
            [
                {"text": "🔙 Actividades", "callback_data": "/int_si_actividades"},
                {"text": "✨ Alternativas", "callback_data": "/int_no_actividades"}
            ],
            [
                {"text": "⏹️ Quieres terminar la sesión", "callback_data": "/int_despedirse"}
            ]
        ]

        mensaje = {
            "text": "¿Quieres seguir practicando estas actividades o prefieres ver otras ideas? \n También podemos cerrar la sesión si ya es suficiente por hoy ",
            "reply_markup": {"inline_keyboard": botones}
        }

        dispatcher.utter_message(json_message=mensaje)
        return []

# class ActionMenuSelActividad(Action):
#     def name(self) -> Text:
#         return "action_menu_sel_actividad"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         botones = [
#             {"title": "🔴 Opción 1", "payload": '/int_sel_actividad{"ent_numActividad":"1"}'},
#             {"title": "🟡 Opción 2", "payload": '/int_sel_actividad{"ent_numActividad":"2"}'},
#             {"title": "🟢 Opción 3", "payload": '/int_sel_actividad{"ent_numActividad":"3"}'},
#             {"title": "⭐ Opción 4", "payload": '/int_sel_actividad{"ent_numActividad":"4"}'},
#             {"title": "📋 Ver todas", "payload": '/int_actividades_mostrarAll{"ent_actividades_all":"false"}'}
#         ]

#         dispatcher.utter_message(
#             text="Elige el número de actividad que te interesa:",
#             buttons=botones
#         )
#         return []


# class ActionMenuNoProfundizarActividades(Action):
#     def name(self) -> Text:
#         return "action_menu_no_profundizar_actividades"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         botones = [
#             {"title": "🔙 Actividades", "payload": "/int_si_actividades"},
#             {"title": "✨ Alternativas", "payload": "/int_no_actividades"},
#             {"title": "⏹️ Quieres terminar la sesión", "payload": "/int_despedirse"}
#         ]

#         dispatcher.utter_message(
#             text="¿Quieres seguir practicando estas actividades o prefieres ver otras ideas?\nTambién podemos cerrar la sesión si ya es suficiente por hoy.",
#             buttons=botones
#         )
#         return []


# ========================================ACTIVIDADES DETALLADAS =========================================================


EJERCICIOS_DETALLADOS = {
    "respiracion": [
        {"texto": "Siéntate derecho, relaja los hombros y coloca las manos sobre tus piernas.", "boton": "➡️ Comenzar"},
        {"texto": "Inhala lentamente por la nariz durante 4 segundos.", "boton": "✅ Inhalé"},
        {"texto": "Mantén la respiración durante 7 segundos.", "boton": "✅ Mantuve"},
        {"texto": "Exhala despacio por la boca durante 8 segundos.", "boton": "✅ Exhalé"},
        {"texto": "Repite 3 veces, sintiendo cómo tu cuerpo se relaja.", "boton": "👌 Listo"}
    ],
    "escritura": [
        {"texto": "Encuentra un lugar tranquilo y sin distracciones.", "boton": "➡️ Siguiente"},
        {"texto": "Escribe lo que sientes durante 10 minutos, sin preocuparte por ortografía o estructura.", "boton": "📝 Terminé"},
        {"texto": "Permítete expresar cualquier emoción que surja.", "boton": "👌 Listo"}
    ],
    "audio": [
        {"texto": "Busca un audio de meditación guiada o sonidos de la naturaleza.", "boton": "🎧 Reproducir"},
        {"texto": "Siéntate o recuéstate cómodamente.", "boton": "😌 Estoy listo"},
        {"texto": "Escucha durante 5 minutos, concentrándote en tu respiración.", "boton": "👌 Terminé"}
    ],
    "estiramientos": [
        {"texto": "Ponte de pie y relaja los hombros.", "boton": "➡️ Siguiente"},
        {"texto": "Realiza movimientos suaves de cuello, hombros, brazos y espalda durante 2-3 minutos.", "boton": "✅ Hecho"},
        {"texto": "Respira profundamente mientras te estiras.", "boton": "👌 Listo"}
    ],
    "baile": [
        {"texto": "Elige una canción que te guste.", "boton": "🎵 Listo"},
        {"texto": "Muévete a tu ritmo, sin preocuparte por cómo se ve.", "boton": "💃 Bailando"},
        {"texto": "Disfruta de cada movimiento y concéntrate en la música.", "boton": "👌 Terminé"}
    ],
    "gratitud": [
        {"texto": "Toma papel y lápiz.", "boton": "📝 Listo"},
        {"texto": "Escribe 3 cosas por las que te sientas agradecido hoy.", "boton": "🙏 Hecho"},
        {"texto": "Pueden ser detalles pequeños o grandes logros.", "boton": "👌 Terminé"}
    ],
    "proyecto": [
        {"texto": "Elige una actividad creativa: dibujar, escribir, cocinar, etc.", "boton": "🎨 Listo"},
        {"texto": "Dedica 15 minutos a disfrutar el proceso.", "boton": "⌛ Terminé"},
        {"texto": "Concéntrate en tu disfrute, sin presionarte.", "boton": "👌 Hecho"}
    ],
    "compartir": [
        {"texto": "Piensa en alguien cercano.", "boton": "🤔 Lo tengo"},
        {"texto": "Envía un mensaje amable o de agradecimiento.", "boton": "💌 Enviado"},
        {"texto": "Observa cómo este gesto te hace sentir.", "boton": "👌 Listo"}
    ],
    "meditacion": [
        {"texto": "Siéntate cómodamente y cierra los ojos.", "boton": "🧘 Estoy listo"},
        {"texto": "Concéntrate en tu respiración durante 3 minutos.", "boton": "⌛ Terminé"},
        {"texto": "Observa tus pensamientos sin juzgarlos.", "boton": "👌 Listo"}
    ],
    "organizar": [
        {"texto": "Escoge un área pequeña: escritorio, habitación o cajón.", "boton": "📦 Listo"},
        {"texto": "Ordena y limpia durante unos minutos.", "boton": "🧹 Terminé"},
        {"texto": "Respira profundo y observa el cambio.", "boton": "👌 Hecho"}
    ],
    "leer": [
        {"texto": "Escoge un libro, artículo o cita breve.", "boton": "📖 Tengo uno"},
        {"texto": "Lee durante unos minutos.", "boton": "⌛ Terminé"},
        {"texto": "Concéntrate en el contenido y disfruta de la lectura.", "boton": "👌 Listo"}
    ],
    "hidratacion": [
        {"texto": "Toma un vaso de agua.", "boton": "💧 Listo"},
        {"texto": "Bébelo lentamente, prestando atención a cada sorbo.", "boton": "🥤 Terminé"},
        {"texto": "Respira profundo mientras lo haces.", "boton": "👌 Hecho"}
    ]
}

# ------------------------------
# Refuerzos positivos
# ------------------------------
REFUERZOS_PASOS = [
    "💪 ¡Muy bien! Sigamos adelante.",
    "✨ Estás haciéndolo excelente.",
    "🌟 Paso a paso vas logrando más calma.",
    "🙌 Lo estás logrando, continúa así."
]

REFUERZOS_FINALES = [
    "🎉 ¡Excelente trabajo, completaste el ejercicio!",
    "🌸 Cada práctica te ayuda a sentirte mejor.",
    "💖 Estoy orgulloso de tu esfuerzo, sigue así.",
    "🌈 Notarás más calma y claridad mental."
]

# ------------------------------
# Acción para mostrar pasos
# ------------------------------
class ActionEjercicioDetallado(Action):
    def name(self) -> Text:
        return "action_ejercicio_detallado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        varEjercicio = tracker.get_slot("slot_ejercicio_actual")
        paso = tracker.get_slot("slot_paso_actual") or 0

        if varEjercicio not in EJERCICIOS_DETALLADOS:
            dispatcher.utter_message(text="No se encontró el ejercicio seleccionado.")
            return []

        pasos = EJERCICIOS_DETALLADOS[varEjercicio]

        # Caso: ejercicio finalizado
        if paso >= len(pasos):
            refuerzo_final = random.choice(REFUERZOS_FINALES)
            dispatcher.utter_message(text=f"{refuerzo_final} 🌟")

            # Mostrar el menú de opciones reutilizando la acción existente
            ActionMenuNoProfundizarActividades().run(dispatcher, tracker, domain)

            return [SlotSet("slot_paso_actual", 0), SlotSet("slot_ejercicio_actual", None)]

        # Obtenemos el paso con texto y botón
        paso_info = pasos[paso]
        texto = paso_info["texto"]
        titulo_boton = paso_info["boton"]
        paso_siguiente = paso + 1

        # Agregamos un refuerzo positivo al texto del paso
        # refuerzo = random.choice(REFUERZOS_PASOS)
        # texto_con_refuerzo = f"{texto}\n\n{refuerzo}"
        texto_con_refuerzo = texto

        dispatcher.utter_message(
            text=texto_con_refuerzo,
            buttons=[{
                "title": titulo_boton,
                "payload": f'/int_paso_listo{{"ent_paso_actual": {paso_siguiente}}}'
            }]
        )

        return [SlotSet("slot_paso_actual", paso_siguiente)]
