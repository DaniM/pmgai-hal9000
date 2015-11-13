import halchat

DOOR_TRANSITIONS = [('open', ['closed'], 'opened'), ('close', ['opened'], 'closed')]
LIGHTS_TRANSITIONS = [('turn on', ['off'], 'on'), ('switch on', ['off'], 'on'), ('turn off', ['on'], 'off'),
                      ('switch off', ['on'], 'off')]

WORLD = {'map': ['kitchen', 'bridge', 'bedroom'],
         'devices': {
             'kitchen': ['bridge door', 'bedroom door', 'lights', 'door','door to the bedroom'],
             'bridge': [],
             'bedroom': []
         },
         'kitchen': {
             'door' : [ 'bridge door', 'bedroom door' ], # when one object can refer to another or more than one put it on a list
             'door to the bedroom' : ['bedroom door'],
             'bridge door': {'transitions': DOOR_TRANSITIONS, 'state': 'closed'},  # model devices as some kind of fsm
             'bedroom door': {'transitions': DOOR_TRANSITIONS, 'state': 'closed'},
             'lights': {'transitions': LIGHTS_TRANSITIONS, 'state': 'off'}
         }
         }

HAL9000_RESPONSES = [
    # where am i? first
    (r'Where am I?', halchat.WhereAmIResponse.Respond),
    (r'You are (worrying|scary|disturbing)',  # Pattern 1.
     ['Yes, I am %1.',  # Response 1a.
      'Oh, sooo %1.']),

    (r'Are you ([\w\s]+)\?',  # Pattern 2.
     ["Why would you think I am %1?",  # Response 2a.
      "Would you like me to be %1?"]),

    (r'',  # Pattern 3. (default)
     ["Is everything OK?",  # Response 3a.
      "Can you still communicate?"])
]


class InteractiveObject:
    def __init__(self, world):
        pass

    def interact(self, match):
        pass
