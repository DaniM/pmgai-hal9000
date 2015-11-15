import time
import speech_recognition as sr
import threading
import sys
import win32com

class HALInput(object):
    def __init__(self, agent):
        self.agent = agent

    def on_input(self,evt):
        self.agent.on_input(evt)

    def on_command(self,evt):
        self.agent.on_command(evt)

class TerminalInput(HALInput):
    def __init__(self, agent, terminal):
        super(TerminalInput, self).__init__(agent)
        self.terminal = terminal
        self.terminal.events.user_input.connect(self.on_input)
        self.terminal.events.user_command.connect(self.on_command)

class TextAndVoiceInput(TerminalInput):
    def __init__(self,agent,terminal):
        super(TextAndVoiceInput, self).__init__(agent,terminal)

        # For speech recognition - first create a listener
       # self.listener = win32com.client.Dispatch("SAPI.SpSharedRecognizer")

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1000
        self._stop = False

        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._stop = True
        self.thread.join()

    def listen(self):
        """Entry point for the speech-to-text thread."""
        time.sleep(0.1)

        for st in self.sentences():
            self.terminal.text_buffer += st
            self.terminal.show_input( self.terminal.text_buffer )

    def sentences(self):
        while not self._stop:
            with sr.Microphone() as source:
                print("Listening to microphone...")
                audio = self.recognizer.listen(source)
            try:
                print("Received %i bytes of audio data." % len(audio.frame_data))
                sentence = self.recognizer.recognize_google(audio)
                print("Understood: %s" % sentence)
                yield sentence

            except LookupError:
                print("Recognizer could not understand.")
                yield ""
            except:
                print("Unexpected error:", sys.exc_info()[0])
                yield ""
