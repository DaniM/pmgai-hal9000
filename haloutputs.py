import win32com.client



# little wrappers for voice and text

class HALOutput:
    def puts(self,output):
        pass

    def set_output_params(self,params):
        pass

class TerminalWindowWrapper(HALOutput):
    def __init__(self,terminal):
        self.terminal = terminal
        self.alignment = 'left'
        self.color = '#1463A3'

    def puts(self,out):
        self.terminal.log(out,self.alignment,self.color)

    def set_output_params(self,params):
        if 'align' in params:
            self.alignment = params['align']
        if 'color' in params:
            self.color = params['color']

class VoiceOutputWrapper(HALOutput):
    def __init__(self):
        self.voice = win32com.client.Dispatch("SAPI.SpVoice")

    def puts(self,out):
        self.voice.Speak(out)

class VoiceAndTextOutput(HALOutput):
    def __init__(self,terminal):
        self.text = TerminalWindowWrapper(terminal)
        self.voice = VoiceOutputWrapper()

    def set_output_params(self,params):
        self.text.set_output_params(params)
        self.voice.set_output_params(params)

    def puts(self,output):
        self.text.puts(output)
        self.voice.puts(output)