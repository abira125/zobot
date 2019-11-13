from rasa_core.channels.webexteams import WebexTeamsInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from rasa_core.utils import EndpointConfig


# load your trained agent
nlu_interpreter = RasaNLUInterpreter('./models/current/nlu')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/current/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)

input_channel = WebexTeamsInput(
    access_token=# this is the `bot access token`
    room=# the name of your channel to which the bot posts (optional)
)

# set serve_forever=True if you want to keep the server running
agent.handle_channels([input_channel], 5004, serve_forever=True)
