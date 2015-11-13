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
        self.agent.out.set_output_params( {'align':'left', 'color':'#ff3000'} )
        self.agent.out.puts('Command `{}` unknown.'.format(evt.text))
        self.agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
        self.agent.terminal.log("I'm afraid I can't do that.")


class HALQuitCommand(HAL9000Command):
    """Quit command
    """
    def __init__( self, name, agent ):
        super( HALQuitCommand, self ).__init__( name, agent );

    def executeCommand(self,evt,world):
        vispy.app.quit()

###########################################
# let's use use some closures for practice!
############################################

#relocate command
def RelocateCommandFactory( agent ):
    def Command(evt,world):
        agent.location = evt.text[9:]
        agent.out.set_output_params( {'align':'center', 'color':'#404040'} )
        agent.out.puts('\u2014 Now in the {}. \u2014'.format(agent.location))
    return Command

# Previous ones as closures
def UnrecognizedCommandFactory( agent ):
    def Command(evt,world):
        agent.out.set_output_params( {'align':'left', 'color':'#ff3000'} )
        agent.out.puts('Command `{}` unknown.'.format(evt.text))
        agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
        agent.out.puts("I'm afraid I can't do that.")
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
    agent.out.set_output_params( {'align':'left', 'color':'#ff3000'} )
    agent.out.puts('Command `{}` unknown.'.format(match['command']))
    agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
    agent.out.puts("I'm afraid I can't do that.")

def RelocateCommand(agent,world,match):
    location = match['location']
    if location in world['map']:
        if agent.location == location:
            agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
            agent.out.puts('You are in the {} already.'.format(agent.location))
        else:
            agent.location = location
            agent.out.set_output_params( {'align':'center', 'color':'#404040'} )
            agent.out.puts('')
            agent.out.puts('\u2014 Now in the {}. \u2014'.format(agent.location))
    else:
        agent.terminal.log("That room doesn't exist", align='right', color='#00805A')

def QuitCommand(agent,world,match):
    vispy.app.quit()

def SimpleInteractCommand( agent, world, match ):
    object_name = match['object']
    interaction = match['verb']
    if object_name in world['devices'][agent.location]:
        # the object exists, can we interact with it?
        obj = world[agent.location][object_name]

        # check if it's a list (we have to enumerate)
        if isinstance(obj,list):
            if len(obj) > 1:
                #TODO: create a closure and push it as context for the next input
                agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
                agent.out.puts("Which one? {0}".format(str(obj)))
            else:
                #it refers to another object, recursive call
                match['object'] = obj[0]
                SimpleInteractCommand(agent, world, match)
        else:
            # can interact?
            transitions = obj['transitions']
            for t in transitions:
                if t[0] == interaction:
                    # now check if we are on the state already
                    if t[2] != obj['state']:
                        if obj['state'] in t[1]:
                            agent.out.set_output_params( {'align':'center', 'color':'#404040'} )
                            agent.out.puts('')
                            obj['state'] = t[2]
                            agent.out.puts('\u2014 {0} {1}. \u2014'.format(object_name, obj['state']))
                        else:
                            agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
                            agent.out.puts('{0} {1}. Can\'t {0}'.format(object_name, obj['state'], interaction))
                    else:
                        agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
                        agent.out.puts("{0} {1} already".format(object_name,obj['state']))
                    return
            agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
            agent.out.puts('Can\'t {0} {1}'.format(interaction,object_name))
    else:
        agent.out.set_output_params( {'align':'right', 'color':'#00805A'} )
        agent.out.puts("No {0} to {1}".format(object_name,interaction))



COMMANDS = [ 
    #(r'(?P<verb>turn (?P<verb2>on|off)) (the)? (?P<object>[\w\s0-9]+) .*', ),
    #(r'(?P<verb>turn) the? (?P<object>[\w\s0-9]+) (?P<verb2>on|off) .*', )
    (r'(?P<verb>open)(\sthe)? (?P<object>[\w\s0-9]+)(\s.*|please)?', SimpleInteractCommand ),
    (r'(?P<verb>close)(\sthe)? (?P<object>[\w\s0-9]+)(\s.*|please)?', SimpleInteractCommand ),
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
                command(agent,world,match.groupdict())
                break
    return Command
            

