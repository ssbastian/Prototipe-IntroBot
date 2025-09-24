from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher



from actions.db import guardarUsuario


#SALUDOS
class ActionGuardarNombre(Action):

    def name(self) -> Text:
        return "action_guardar_nombre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        varNombre = tracker.get_slot("slot_name")
        sender_id = tracker.sender_id  # <- este es el ID único del usuario
        
        if not varNombre:
            dispatcher.utter_message(text="No entendí tu varNombre, ¿puedes repetirlo?")
            return []

        guardarUsuario(sender_id, varNombre)

        #dispatcher.utter_message(text=f"Gracias, {varNombre}, he guardado tu nombre")
        dispatcher.utter_message(response ="utter_nombre_guardado")
        
        return [
            SlotSet("slot_name", varNombre),
            SlotSet("slot_usuario_nuevo", False)
        ]

 
class ActionPreguntarEmocion(Action):
    def name(self):
        return "action_preguntar_emocion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Definimos las opciones válidas

        self.valid_choices = {
            "😊 Feliz": "feliz",
            "😌 Tranquilo": "tranquilo",
            "😍 Emocionado": "emocionado",
            "😢 Triste": "triste",
            "😟 Ansioso": "ansioso",
            "😡 Enojado": "enojado",
            "😔 Inseguro": "inseguro",
            "😴 Cansado": "cansado",
            "😐 Neutral": "neutral"
        }

        # Configuración del teclado
        reply_markup = {
            "keyboard": [list(self.valid_choices.keys())[i:i+3] for i in range(0, len(self.valid_choices), 3)],
            "resize_keyboard": True,
            "one_time_keyboard": True,
            "input_field_placeholder": "⚠️ Usa solo los botones ⬇️",
            "is_persistent": True
        }
        # Mensaje inicial
        message = {
            "text": "Para adaptar las actividades a cómo te sientes hoy, ¿cómo describirías tu nivel de comfort frente a situaciones sociales en este momento?",
            "reply_markup": reply_markup,
            "parse_mode": "Markdown"
        }
        dispatcher.utter_message(json_message=message)
        
        return []
    
class ActionExplicarIntroversion(Action):
    def name(self) -> Text:
        return "action_explicar_introversion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("entrando a EXPLICARinTROVERSION------")
        last_intent = tracker.get_intent_of_latest_message()
        if last_intent == "int_afirmar_saludo":
            texto = ("¡Genial! Igual te lo explico brevemente: "
                     "la introversión es una forma natural de ser. "
                     "Disfrutas más de la calma y puedes sentirte agotado "
                     "en situaciones sociales intensas. ¿Así entendido?")
        else:
            texto = ("No pasa nada, te lo explico brevemente: "
                     "la introversión es una forma natural de ser. "
                     "Disfrutas más de la calma y puedes sentirte agotado "
                     "en situaciones sociales intensas. ¿Así entendido?")
        
        dispatcher.utter_message(
            text=texto,
            buttons=[{"title": "Entendido", "payload": "/int_entendido_saludo"}]
        )
        return []
    
    
    