![logo](docs/images/bot.PNG)

# Zobot: A Restaurant Chatbot
Works with [Zomato](https://www.zomato.com/who-we-are) and [Slack](https://slack.com/intl/en-in/) to get your favourite local restaurants

### Introduction

This is a restaurant chatbot that helps the user to find a resturant of his/her liking based on food preferences 

It engages the user in a conversation to understand the following preferences:
1) Cuisine
2) Budget
3) Location

It passes on this information to [Zomato's APIs](https://developers.zomato.com/documentation) to fetch the relevant restaurants. The top 5 restaurants are then served to the user through chat. The user can also ask the list to be sent through email.

### Demo
A short 6 minute demo can be found [here](https://www.youtube.com/watch?v=VAp8tO254Yc) highlighting the various flows and Slack integration

### Installation

Download this repo and cd into the folder

Install the dependencies
$ pip install -r requirements.txt

Install the spacy library
pip install rasa_nlu[spacy]

Create softlinks
python -m spacy download en_core_web_md
python -m spacy link en_core_web_md en

### Training the RASA  NLU

In order to train the interpreter, run the following command
$ python -m rasa_nlu.train -c nlu_config.yml --data data/data.json -o models --fixed_model_name nlu --project current --verbose

### Training the RASA CORE
In order to train RASA CORE, run the following command
$ python -m rasa_core.train -d domain.yml -s data/stories.md -o models/current/dialogue -c policies.yml

### Running the action server (this is a pre-requisite for CLI)

In order to run rasa action server, execute
$ python -m rasa_core_sdk.endpoint --actions actions

### Running chatbot on CLI
In order to run rasa at commandline, execute
$ python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml
