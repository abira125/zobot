# Chatbot for restaurant search

### Introduction

In a coversation with the user, this bot gathers the kind of restaurant they are looking for, in terms of cuisine, budget and location. It then uses Zomato APIs to get the relevant restaurants and forwards it to the user's email    

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
