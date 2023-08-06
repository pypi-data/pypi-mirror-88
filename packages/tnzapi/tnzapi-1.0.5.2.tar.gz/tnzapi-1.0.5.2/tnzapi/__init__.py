from tnzapi import _config

class TNZAPI():

    def __init__(self, **kwargs):
        for key, value in kwargs.items():

            if key == "Sender":
                self.Sender = _config.__Sender__ = value

            if key == "APIKey":
                self.APIKey = _config.__APIKey__ = value

        self._send = None
        self._get = None
        self._set = None

    @property
    def Send(self, **kwargs):

        """ tnzapi.send.__init__.py - Send() """

        if self._send == None:
            from tnzapi.send import Send

            self._send = Send(**kwargs)

        return self._send

    @property
    def Get(self, **kwargs):
    
        """ tnzapi.get._reference.py - Reference() """
        
        if self._get == None:
            from tnzapi.get import Get
            self._get = Get(**kwargs)
    
        return self._get

    @property
    def Set(self, **kwargs):

        """ tnzapi.set._reference.py - Reference() """

        if self._set == None:
            from tnzapi.set import Set
            self._set = Set(**kwargs)
    
        return self._set