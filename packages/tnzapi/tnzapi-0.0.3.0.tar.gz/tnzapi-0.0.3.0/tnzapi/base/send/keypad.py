import json

from tnzapi.base.functions import Functions

class Keypad(object):

    def __init__(self, **kwargs):

        self.Tone        = 0
        self.RouteNumber = ""
        self.Play        = ""
        self.PlayFile    = ""

        for key, value in kwargs.items():

            if key == "Tone":
                self.Tone = value

            if key == "RouteNumber":
                self.RouteNumber = value
            
            if key == "Play":
                self.Play = value
            
            if key == "PlayFile":
                self.PlayFile = value

    """ Data """
    @property
    def Data(self):

        return {
            "Tone": self.Tone,
            "RouteNumber": self.RouteNumber,
            "Play": self.Play
        }

    @property
    def Tone(self):
        return self._Tone
    
    @Tone.setter
    def Tone(self,val):
        self._Tone = val
    
    @property
    def RouteNumber(self):
        return self._RouteNumber
    
    @RouteNumber.setter
    def RouteNumber(self,val):
        self._RouteNumber = val

    @property
    def Play(self):
        return self._Play
    
    @Play.setter
    def Play(self,val):
        self._Play = val

    @property
    def PlayFile(self):
        return self._PlayFile
    
    @PlayFile.setter
    def PlayFile(self,val):
        self._PlayFile = val

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)
