from tnzapi import _config
from tnzapi.base.functions import Functions

class Common:

    Sender          = _config.__Sender__
    APIKey          = _config.__APIKey__
    APIVersion      = _config.__APIVersion__
    APIURL          = _config.__APIURL__ + "/get/"
    APIHeaders      = _config.__APIHeaders__

    MessageID       = ""

    """ Constructor """
    def __init__(self,kwargs):
        
        self.SetArgs(kwargs)

    """ Set Args """
    def SetArgs(self, kwargs):

        if "Sender" in kwargs:
            self.Sender = _config.__Sender__ = kwargs.pop("Sender")

        if "APIKey" in kwargs:
            self.APIKey = _config.__APIKey__ = kwargs.pop("APIKey")
        
        if "MessageID" in kwargs:
            self.MessageID = kwargs.pop("MessageID")
    
    def __pretty__(self,obj):

        return Functions.__pretty__(self,obj)