import requests
import json

from tnzapi.get._common import Common
from tnzapi.base import InboundSMSResult

class InboundSMS(Common):

    TimePeriod  = 1440

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgs(kwargs)

    """ Set Args """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "TimePeriod":
                self.TimePeriod = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "InboundSMS",
            "TimePeriod" : self.TimePeriod
        }


    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL, data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return InboundSMSResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return InboundSMSResult(error=str(e))

        return InboundSMSResult(response=r)

    """ Function to send message """
    def Poll(self, **kwargs):

        self.SetArgs(kwargs)

        if not self.Sender :
            return False
        
        if not self.APIKey :
            return False
        
        if not self.TimePeriod:
            return False
        
        return self.__PostMessage()

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'InboundSMS(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'