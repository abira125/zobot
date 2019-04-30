from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# from rasa_core.actions.action import Action
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

# from rasa_core.events import SlotSet
import json
#from send_mail import email
from zomato_slots import results
from city_check import check_location
from email_config import Config
from flask_mail_check import send_email

from spell_checker import get_correct_word
from texttable import Texttable


from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

class ActionRestart(Action):
	def name(self):
		return 'action_restart'
	def run(self, dispatcher, tracker, domain):
		AllSlotsReset()
		return[Restarted()]

class ActionFallback(Action):

    def name(self):
        return "fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Sorry, didn't get that. Try again.")
        return [AllSlotsReset()]


class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'

	def encodeprice (self, price):
		print ("encodeprice input=", price)

		if price == "lesser than 300" or price == "between 300 to 700" or price == "more than 700":
			return price

		if price.isdigit():
			price = int(price)

			if price < 300:
				return "lesser than 300"
			elif 300 <= price < 700:
				return "between 300 to 700"
			else:
				return "more than 700"
		
	def run(self, dispatcher, tracker, domain):

		dispatcher.utter_message("Fetching results from Zomato, pls wait...\n")

		loc = tracker.get_slot('location')

		cuisine = tracker.get_slot('cuisine')
		price = self.encodeprice(tracker.get_slot('price'))
		print (price)

		global restaurants

		restaurants = results(loc, cuisine, price)
		top10 = restaurants.head(10)
		
		# top 10 results to display
		if len(top10)>0:
			t = Texttable()
			t.header(['Name', 'Rating', 'Address', 'Budget for 2'])
			for index, row in top10.iterrows():
				cur_row = [row["restaurant_name"], row["restaurant_rating"], row["restaurant_address"],row["budget_for2people"]]
				t.add_row(cur_row)
			response=t.draw()
		else:
			response = 'No restaurant found'
			dispatcher.utter_message(response + ". Restart from beginning with Greetings")
			AllSlotsReset()
			return [Restarted()]

		dispatcher.utter_message(response)



class SendMail(Action):
	def name(self):
		return 'email_restaurant_details'
		
	def run(self, dispatcher, tracker, domain):
		recipient = tracker.get_slot('email')

		top10 = restaurants.head(10)
		print("got this correct email is {}".format(recipient))
		send_email(recipient, top10)

		dispatcher.utter_message("Have a great day!")


class Check_location(Action):
	def name(self):
		return 'action_check_location'
		
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		loc = get_correct_word(loc)	#use spell checker to make sure location is correct.
		check = check_location(loc)
		
		return [SlotSet('location',check['location_new']), SlotSet('location_found',check['location_f'])]
		
		
		
		

