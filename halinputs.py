from nltk.chat.util import Chat
from nltk.chat.util import reflections
import random


class HAL9000Response:
    """HAL9000 Response basic interface
	"""

    def __init__(self, agent):
        self.agent = agent

    def respond(self, world):
        pass

    def match(self, evt, world):
        pass


class DefaultResponse(HAL9000Response):
    def __init__(self, agent):
        super(DefaultResponse, self).__init__(agent)
        self.first_time = True

    def match(self, evt, world):
        if self.first_time:
            self.first_time = False
            return 'Hi I\'m HAL9000'
        else:
            return 'Type something else'


class WhereAmIResponse(HAL9000Response):
    """ Response for the \'Where am I?\' question
	"""

    def __init__(self, agent):
        super(WhereAmIResponse, self).__init__(agent)

    def match(self, evt, world):
        text = evt.text.upper()
        if text == 'WHERE AM I?':
            return self.agent.location
        else:
            return None

    def Respond(agent, world, data):
        agent.terminal.log(agent.location, align='right', color='#00805A')


class HAL9000Chatbot(Chat):
    """ Extends the base chat for providing a little more elaborated answers
	"""

    def __init__(self, agent, pairs):
        super(HAL9000Chatbot, self).__init__(pairs, reflections)
        self.agent = agent;

    def add_response(self, pair):
        """Add new responses to the agent database"""
        pass

    def respond(self, text, world):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(text)
            # did the pattern match?
            if match:
                # now check if the answer is callable (a function)
                if callable(response):
                    response(self.agent, world, match)
                else:
                    # do exactly the same as parent
                    # choose a random answer
                    choice = random.choice(response)
                    # process wildcards
                    resp = self._wildcards(choice, match)
                    # fix munged punctuation at the end
                    if resp[-2:] == '?.': resp = resp[:-2] + '.'
                    if resp[-2:] == '??': resp = resp[:-2] + '?'
                    self.agent.terminal.log(resp, align='right', color='#00805A')
                return
