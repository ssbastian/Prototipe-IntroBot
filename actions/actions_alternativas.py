from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher




class ActionMenuRecurso(Action):
    def name(self) -> Text:
        return "action_menu_recurso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Primero mostrar el mensaje con los recursos disponibles
        dispatcher.utter_message(
            text="Mirá por el momento tengo estos recursos disponibles para ti:\n"
                 "1️⃣ Meditación guiada (5 min)\n"
                 "2️⃣ Ejercicios de respiración\n"
                 "3️⃣ Artículo sobre manejo emocional"
        )

        # Luego mostrar los botones de selección
        botones = [
            {"title": "Boton 1️⃣", "payload": '/int_menu_sel_recurso{"ent_tipo_recurso":"meditacion"}'},
            {"title": "Boton 2️⃣", "payload": '/int_menu_sel_recurso{"ent_tipo_recurso":"respiracion"}'},
            {"title": "Boton 3️⃣", "payload": '/int_menu_sel_recurso{"ent_tipo_recurso":"articulo"}'}
        ]

        slot_name = tracker.get_slot("name") or "amigo"
        
        dispatcher.utter_message(
            text=f"{slot_name} ¿qué recurso te gustaria conocer?",
            buttons=botones
        )
        
        return []
    
    
class ActionMenuAlternativa(Action):
    def name(self) -> Text:
        return "action_menu_alternativa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        botones = [
            {"title": "🤖 Hablar", "payload": '/int_menu_sel_alternativa{"ent_tipo_alternativa":"sentimientos"}'},
            {"title": "📚 Recurso", "payload": '/int_menu_sel_alternativa{"ent_tipo_alternativa":"recursos"}'},
            {"title": "⏹️ Terminar sesión", "payload": '/int_despedirse'}
        ]

        dispatcher.utter_message(
            text="¿Te gustaría en cambio...",
            buttons=botones
        )
        
        return []


#ALTERNATIVA 1
class ActionResponderEscuchaActiva(Action):
    def name(self) -> Text:
        return "action_responder_escucha_activa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("ENTRANDO a accion escucha activa-----")
        #varEmocion = tracker.get_slot("slotEmocion")
        varEmocion = "ansioso"

        respuestas = {
            "triste": "Parece que has estado pasando por un momento difícil, y me alegra que quieras hablarlo.",
            "ansioso": "Debe ser agotador sentir esa ansiedad. Estoy aquí para escucharte sin juzgar.",
            "feliz": "¡Me alegra que te sientas así! Cuéntame más, ¿qué ha hecho que tu día sea especial?",
        }

        mensaje = respuestas.get(varEmocion, 
            "Gracias por confiar en mí para hablar de esto. Cuéntame, ¿qué tienes en mente?")
        dispatcher.utter_message(text=mensaje)
        return []



#ALTERNATIVA 2

class ActionManejarAlternativas(Action):
    def name(self) -> Text:
        return "action_manejar_alternativas"
    
    def run(self, dispatcher, tracker, domain):
        varOpcion = tracker.get_slot("slot_tipo_alternativa")  # Lee el slot específico
        print("entrando a la action varOpcion",varOpcion)
        if varOpcion == "sentimientos":
            dispatcher.utter_message(text="------sentiminetos ha sido seleccionado-----")
            dispatcher.utter_message(response="utter_iniciar_escucha")
            #ActionResponderEscuchaActiva().run(dispatcher, tracker, domain)
            return [
                SlotSet("slot_tipo_alternativa", None),
                SlotSet("slot_contexto", "escucha_activa")  # <- aquí marcamos el contexto
            ]
        elif varOpcion == "recursos":
            print("seleccionaste recursos------")  
            # dispatcher.utter_message(response="utter_menu_list_recurso")
            # dispatcher.utter_message(response="utter_menu_button_recurso") #payload
            return [FollowupAction("action_menu_recurso"),
                    SlotSet("slot_tipo_alternativa", None),
                    SlotSet("slot_contexto", None)]
        elif varOpcion == "despedida":
            dispatcher.utter_message(response="utter_usuario_se_despiede")
            return [SlotSet("slot_tipo_alternativa", None),
                    SlotSet("slot_contexto", None)]    
        else:
            dispatcher.utter_message(text="Opción no reconocida.")
            return [SlotSet("slot_tipo_alternativa", None),
                    SlotSet("slot_contexto", None)]
        
  


## Seleccion y entrega de recurso      

class ActionEntregaRecursoSel(Action):
    def name(self) -> Text:
        return "action_entrega_recurso_sel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        varTipoRecurso = tracker.get_slot("slot_tipo_recurso")
        print("varTipoRecurso: ",varTipoRecurso)
        
        recursos = {
            "meditacion": {
                "text": "Aquí tienes un articulo sobre meditación guiada: https://introvertdear.com/news/how-meditation-helps-me-thrive-as-an-introvert/"
              , "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400"
            },
            "respiracion": {
                "text": "Ejercicios de respiración para calmar la ansiedad: https://www.healthline.com/health/anxiety-exercises#thought-cycle",
                "image": "https://images.unsplash.com/photo-1518604666860-9ed391f76460?w=400"
            },
            "articulo": {
                "text": "Aquí tienes una guía sobre cómo superar la ansiedad social siendo introvertido:\nhttps://www.happinessinsolitude.com/articles/effective-strategies-overcoming-social-anxiety-introverts/",
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"
            }
        }
        
        recurso = recursos.get(varTipoRecurso)

        if not recurso:
            dispatcher.utter_message(text="Lo siento, no tengo ese recurso disponible ahora.")
            return []
             
        dispatcher.utter_message(
            text=recurso["text"],
            image=recurso["image"]
        )
        
        dispatcher.utter_message(
            text = "¡Excelente! espero Disfrutes ese recurso y para que mas adelante me cuentes qué te pareció🌟"
        )
        # Llamar automáticamente al menú de opciones
        return [
            SlotSet("slot_tipo_recurso", None),
            FollowupAction("action_menu_no_profundizar_actividades")
        ]









