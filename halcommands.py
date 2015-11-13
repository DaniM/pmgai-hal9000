import vispy

import re

class HAL9000Command:
    """Base interface for hal commands
    """
    def __init__(self, name, agent):
        self.name = name
        self.agent = agent

    def executeCommand(self, evt, world):
        pass

class HALUnrecognizedCommand(HAL9000Command):
    """Default command when none of the others match
    """
    def __init__( self, name, agent ):
        super( HALUnrecognizedCommand, self ).__init__( name, agent );

    def executeCommand(self,evt,world):
        self.agent.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
        self.agent.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')


class HALQuitCommand(HAL9000Command):
    """Quit command
    """
    def __init__( self, name, agent ):
        super( HALDefaultCommand, self ).__init__( name, agent );

    def executeCommand(self,evt,world):
        vispy.app.quit()

###########################################
# let's use use some closures for practice!
############################################

#relocate command
def RelocateCommandFactory( agent ):
    def Command(evt,world):
        agent.location = evt.text[9:]
        agent.terminal.log('', align='center', color='#404040')
        agent.terminal.log('\u2014 Now in the {}. \u2014'.format(agent.location), align='center', color='#404040')
    return Command

# Previous ones as closures
def UnrecognizedCommandFactory( agent ):
    def Command(evt,world):
        agent.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
        agent.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')
    return Command

def QuitCommandFactory(agent):
    def Command(evt,world):
        vispy.app.quit()
    return Command

##########################################
# Use chatbot to match supported commands
##########################################

# let's redefine commands again in order to have a common interface

def UnrecognizedCommand(agent,world,match):
    agent.terminal.log('Command `{}` unknown.'.format(match.group('command')), align='left', color='#ff3000')    
    agent.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')

def RelocateCommand(agent,world,match):
    location = match.group('location')
    if location in world['map']:
        if agent.location == location:
            agent.terminal.log('You are in the {} already.'.format(agent.location), align='right', color='#00805A')
        else:
            agent.location = location
            agent.terminal.log('', align='center', color='#404040')
            agent.terminal.log('\u2014 Now in the {}. \u2014'.format(agent.location), align='center', color='#404040')
    else:
        agent.terminal.log("That room doesn't exist", align='right', color='#00805A')

def QuitCommand(agent,world,match):
    vispy.app.quit()

def InteractCommand( agent, world, match ):
    object_name = match.group( 'object' )
    if object_name in world[agent.location]:
        # the object exists, can we interact with it?
        obj = world[agent.location][object_name]


COMMANDS = [ 
    #(r'(?P<verb1>turn (?P<verb2>on|turn)) (the)? (?P<object>[\w\s0-9]+) .*', ), 
    #(r'(?P<verb1>turn) (the)? (?P<object>[\w\s0-9]+) (?P<verb2>on|off) .*', )
    #(r'(?P<verb>open) (the)? (?P<object>[\w\s0-9]+) .*', ), 
    #(r'(?P<verb>close) (the)? (?P<object>[\w\s0-9]+) .*', ),
    (r'quit(\s.*)?',QuitCommand),
    (r'relocate (?P<location>\w[\w\s0-9]+)',RelocateCommand),
    (r'(?P<command>[^\s]+).*', UnrecognizedCommand) ]

# the commands executioner
def ChatbotCommands(agent, commands):
    _commands = [(re.compile(x, re.IGNORECASE),y) for (x,y) in commands]
    def Command(evt,world):
        for (pattern,command) in _commands:
            match = pattern.match(evt.text)
            if match:
                command(agent,world,match)
                break
    return Command
            

