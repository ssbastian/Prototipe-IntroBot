# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import random

class ActionMotivacion(Action):
    def name(self):
        return "action_motivacion_personalizada"

    def run(self, dispatcher, tracker, domain):
        frases = [
            "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
            "No te compares con los demás, solo compite contigo mismo.",
            "A veces, el paso más pequeño en la dirección correcta se convierte en el más grande de tu vida."
        ]
        mensaje = random.choice(frases)
        dispatcher.utter_message(text=mensaje)
        return []


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
