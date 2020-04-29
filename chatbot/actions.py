# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import csv
import requests
import json

"""class ActionGotInfo(Action):

	def name(self):
		return "action_got_info"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
		u_name = tracker.get_slot("name")
		u_age = tracker.get_slot("age")
		u_gender = tracker.get_slot("gender")
		dispatcher.utter_message("Just to confirm, your name is {}, age is {} and gender is {}.".format(u_name,u_age,u_gender))
		return []"""

class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Sorry, I couldn't understand.")

class InformForm(FormAction):
	def name(self):
		return "user_form"

	@staticmethod
	def required_slots(tracker: Tracker):
		#A list of required slots that the form has to fill
		#The slot names are given below
		return ["name", "age", "gender", "occupation", "email", "bothering", "mood", "physical", "exp"]

	#Optional method used to map the entities to intents 
	def slot_mappings(self):
		return {"name": self.from_entity(entity = "name", 
										intent = ["reply_name"]), 
				"age": self.from_entity(entity = "age",
										intent = ["reply_age"]),
				"gender": self.from_entity(entity = "gender",
											intent = ["reply_gender"]),
				"occupation": self.from_entity(entity = "occupation",
												intent = ["reply_occupation"]),
				"email": self.from_entity(entity = "email",
											intent = ["reply_email"]),
				"bothering": self.from_entity(entity = "feeling",
											intent = ["reply_bothering"]),
				"mood": self.from_entity(entity = "emotion",
											intent = ["reply_mood"]),
				"physical": self.from_entity(entity = "physical",
												intent = ["reply_physical"]),
				"exp": self.from_entity(entity = "exp",
										intent = ["reply_exp"])}

	def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
		u_name = tracker.get_slot("name")
		u_age = tracker.get_slot("age")
		u_gender = tracker.get_slot("gender")
		u_occupation = tracker.get_slot("occupation")
		u_email = tracker.get_slot("email")
		u_bothering = tracker.get_slot("bothering")
		u_mood = tracker.get_slot("mood")
		u_physical = tracker.get_slot("physical")
		u_exp = tracker.get_slot("exp")

		with open('meh_data.csv', 'a+', newline="") as f:
			writer = csv.writer(f)
			writer.writerow([u_name, u_age, u_gender, u_occupation, u_email, u_bothering, u_mood, u_physical, u_exp])
		message = str(u_bothering) + "is on my mind. " +"I am "+ str(u_mood)+". I face physical issues like "+ str(u_physical)+". "+str(u_exp)
		para = json.dumps(message)
		x = requests.post('http://127.0.0.1:5000/predict', data=para)
		dispatcher.utter_message(text="I think you have "+str(x.text))
		
		return []

