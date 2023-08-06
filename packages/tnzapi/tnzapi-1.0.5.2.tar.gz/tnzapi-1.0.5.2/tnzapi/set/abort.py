import requests
import json

from tnzapi.set._common import Common
from tnzapi.base import SetRequestResult

class Abort(Common):

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgs(kwargs)

    """ Update Data """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "Abort",
            "MessageID" : self.MessageID
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL, data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return SetRequestResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return SetRequestResult(error=str(e))
        
        return SetRequestResult(response=r)

    """ Function to send message """
    def SendRequest(self,**kwargs):

        self.SetArgs(kwargs)

        if not self.Sender :
            return SetRequestResult(error="Empty Sender")
        
        if not self.APIKey :
            return SetRequestResult(error="Empty API Key")
        
        if not self.MessageID:
            return SetRequestResult(error="Empty Message ID")
        
        return self.__PostMessage()

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Abort(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'