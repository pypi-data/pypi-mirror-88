class Send(object):

    def __init__(self):
        self._email = None
        self._fax = None
        self._sms = None
        self._tts = None
        self._voice = None

    def Email(self,**kwargs):

        if self._email == None:
            from tnzapi.send.email import Email
            self._email = Email(kwargs)

        return self._email
    
    def Fax(self,**kwargs):

        if self._fax == None:
            from tnzapi.send.fax import Fax
            self._fax = Fax(kwargs)

        return self._fax

    def SMS(self,**kwargs):

        if self._sms == None:
            from tnzapi.send.sms import SMS
            self._sms = SMS(kwargs)

        return self._sms

    def TTS(self,**kwargs):

        if self._tts == None:
            from tnzapi.send.tts import TTS
            self._tts = TTS(kwargs)
        
        return self._tts
    
    def Voice(self,**kwargs):

        if self._voice == None:
            from tnzapi.send.voice import Voice
            self._voice = Voice(kwargs)

        return self._voice