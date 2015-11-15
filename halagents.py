import vispy

import halinputs

import haloutputs

import halcommands

import halchat

import haldata

import random

class HAL9000(object):
    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'unknown'

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        self.terminal.log("Good morning! This is HAL.", align='right', color='#00805A')

    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self.terminal.log('', align='center', color='#404040')
            self.terminal.log('\u2014 Now in the {}. \u2014'.format(evt.text[9:]), align='center', color='#404040')

        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass

class HAL9001(HAL9000):
    """First extension of HAL9000 (beginner's practice task)
    """
    def __init__(self, terminal):
        super(HAL9001,self).__init__(terminal)
        self.out = haloutputs.TerminalWindowWrapper(terminal)
        self.responses = [ halchat.WhereAmIResponse(self), halchat.DefaultResponse(self) ]
        self.commands = { 
                'relocate' : halcommands.RelocateCommandFactory(self), 
                'quit' : halcommands.QuitCommandFactory(self),
                '' : halcommands.UnrecognizedCommandFactory(self) # just name it in order to use later
            }

    def on_input(self,evt):
        for r in self.responses:
            output = r.match(evt,None)
            if output:
                self.out.puts( output, {'align':'right', 'color':'#00805A'})
                break

    def on_command(self,evt):
        # get the command name
        command = evt.text.split( ' ', 1 )[0]
        # and check if it's a registerd command
        if command in self.commands:
            self.commands[command](evt,None)
        else :
            self.commands[''](evt,None)

    def on_output(self,output):
        self.out.puts(output)


class HAL9002(HAL9000):
    """Second extension of HAL9000 (intermediate's practice task)
    """
    def __init__(self, terminal, world):
        super(HAL9002,self).__init__(terminal)
        # choose a random start position
        self.location = random.choice( world['map'] )
        self.world = world
        # use a chat for the input
        self.chatter = halchat.HAL9000Chatbot(self,haldata.HAL9000_RESPONSES)
        #use another one for the commands
        self.cmder = halcommands.ChatbotCommands(self,halcommands.COMMANDS)

        self.out = haloutputs.TerminalWindowWrapper(terminal)

        # greetings
        self.out.set_output_params( {'align':'right', 'color':'#00805A'} )
        self.out.puts( 'Hi this is HAL9000!')

    def on_input(self,evt):
        self.chatter.respond(evt.text,self.world)

    def on_command(self,evt):
        self.cmder(evt,self.world)

    def on_output(self,output):
        self.out.puts(output)

class HAL9003(HAL9000):
    def __init__(self, terminal, world):
        super(HAL9003,self).__init__(terminal)

        # choose a random start position
        self.location = random.choice( world['map'] )
        self.world = world

        # use a chat for the input
        self.chatter = halchat.HAL9000Chatbot(self,haldata.HAL9000_RESPONSES)
        #use another one for the commands
        self.cmder = halcommands.ChatbotCommands(self,halcommands.COMMANDS)

        self.input = halinputs.TextAndVoiceInput(self, terminal)
        self.out = haloutputs.VoiceAndTextOutput(terminal)

        # greetings
        self.out.puts( 'Hi this is HAL!')

    def on_input(self,evt):
        self.chatter.respond(evt.text,self.world)

    def on_command(self,evt):
        self.cmder(evt,self.world)

    def on_output(self,output):
        self.out.puts(output)