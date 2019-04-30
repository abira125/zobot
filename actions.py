from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# from rasa_core.actions.action import Action
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

# from rasa_core.events import SlotSet
import json
# from send_mail import email
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
        return [Restarted()]


class ActionFallback(Action):
    def name(self):
        return "action_utter_fallback"

    def run(self, dispatcher, tracker, domain):
        #print(tracker.latest_message)
        dispatcher.utter_message("Sorry, didn't get that. Please try again.")
        return [AllSlotsReset()]


class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'

    def encodeprice(self, price):
        #print("encodeprice input=", price)

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
        #print("1-", cuisine)
        cuisinelist = ["chinese", "italian", "south indian", "north indian", "mexican", "american"]
        if cuisine is None or cuisine.lower() not in cuisinelist:
            dispatcher.utter_message("Sorry, didn't get the opted cuisine. Setting it to default i.e. \"Chinese\"")
            cuisine = "chinese"
            SlotSet("cuisine", cuisine)

        cuisine = cuisine.lower()
        #print (cuisine)

        price = tracker.get_slot('price')
        if price is None:
            dispatcher.utter_message("Sorry, you have entered wrong budget. Setting it to default i.e. \"[lesser than 300]\"")
            price = "lesser than 300"
            SlotSet("price", price)

        price = self.encodeprice(price)
        #print(price)

        global restaurants

        restaurants = results(loc, cuisine, price)
        top10 = restaurants.head(10)

        # top 5 results to display
        if len(top10) > 0:
            t = Texttable()
            t.header(['Name', 'Rating', 'Address', 'Budget for 2'])
            for index, row in top10.iterrows():
                cur_row = [row["restaurant_name"], row["restaurant_rating"], row["restaurant_address"],
                           row["budget_for2people"]]
                t.add_row(cur_row)
            response = t.draw()
            print("all slot values: {}".format(tracker.current_slot_values()))
            dispatcher.utter_message(response)
            return [SlotSet('restaurants_found','found')]
            
        else:
            response = 'No restaurant found.' 
            #There can be Zomato error also. Please refer to Action server output'
            dispatcher.utter_message(response)
            return [SlotSet('restaurants_found','notfound')]
            #AllSlotsReset()
            #return [Restarted()]

        


class SendMail(Action):
    def name(self):
        return 'email_restaurant_details'

    def run(self, dispatcher, tracker, domain):

        print("restaurants_found slot is {}".format(tracker.get_slot('restaurants_found')))
        print("all slot values: {}".format(tracker.current_slot_values()))

        recipient = tracker.get_slot('email')
        if recipient is not None:
            top10 = restaurants.head(10)
            print("got this correct email is {}".format(recipient))
            send_email(recipient, top10)
            dispatcher.utter_message("Sure. Mail Sent!")
        else:
            dispatcher.utter_message("Aw snap! Some error occured while sending mail!")

class Check_location(Action):
    def name(self):
        return 'action_check_location'

    def run(self, dispatcher, tracker, domain):

        city_dict = ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune', 'Agra',
                     'Ajmer',
                     'Aligarh', 'Allahabad', 'Amravati', 'Amritsar', 'Asansol', 'Aurangabad', 'Bareilly', 'Belgaum',
                     'Bhavnagar', 'Bhiwandi',
                     'Bhopal', 'Bhubaneswar', 'Bikaner', 'Bokaro Steel City', 'Chandigarh', 'Coimbatore', 'Cuttack',
                     'Dehradun', 'Dhanbad',
                     'Durg-Bhilai Nagar', 'Durgapur', 'Erode', 'Faridabad', 'Firozabad', 'Ghaziabad', 'Gorakhpur',
                     'Gulbarga', 'Guntur',
                     'Gurgaon', 'Guwahati‚ Gwalior', 'Hubli-Dharwad', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar',
                     'Jammu', 'Jamnagar', 'Jamshedpur',
                     'Jhansi', 'Jodhpur', 'Kannur', 'Kanpur', 'Kakinada', 'Kochi', 'Kottayam', 'Kolhapur', 'Kollam',
                     'Kota', 'Kozhikode', 'Kurnool',
                     'Lucknow', 'Ludhiana', 'Madurai', 'Malappuram', 'Mathura', 'Goa', 'Mangalore', 'Meerut',
                     'Moradabad', 'Mysore', 'Nagpur', 'Nanded', 'Nashik',
                     'Nellore', 'Noida', 'Palakkad', 'Patna', 'Pondicherry', 'Raipur', 'Rajkot', 'Rajahmundry',
                     'Ranchi', 'Rourkela', 'Salem', 'Sangli', 'Siliguri',
                     'Solapur', 'Srinagar', 'Sultanpur', 'Surat', 'Thiruvananthapuram', 'Thrissur', 'Tiruchirappalli',
                     'Tirunelveli', 'Tiruppur', 'Ujjain', 'Vijayapura',
                     'Vadodara', 'Varanasi', 'Vasai-Virar City', 'Vijayawada', 'Visakhapatnam', 'Warangal']

        city_dict = [x.lower() for x in city_dict]

        loc = tracker.get_slot('location')
        if loc is not None and len(loc) > 0:
            if loc.lower() not in city_dict:
                loc = get_correct_word(loc)  # use spell checker to make sure location is correct.
            check = check_location(loc)

            return [SlotSet('location', check['location_new']), SlotSet('location_found', check['location_f'])]
        else:
            return [SlotSet('location', None), SlotSet('location_found', 'notfound')]

#not used
class Validate_cuisine(Action):
    def name(self):
        return 'action_check_cuisine'
    def run(self, dispatcher, tracker, domain):
        cuisine = tracker.get_slot('cuisine')
        cuisinelist = ["chinese", "italian", "south indian", "north indian", "mexican", "american"]
        if cuisine is None or cuisine.lower() not in cuisinelist:
            dispatcher.utter_message("Sorry, didn't get the opted cuisine. Setting it to default i.e. \"Chinese\"")
