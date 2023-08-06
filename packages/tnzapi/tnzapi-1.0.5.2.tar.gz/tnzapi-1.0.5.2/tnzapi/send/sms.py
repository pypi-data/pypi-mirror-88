import requests
import json

from tnzapi.send._common import Common
from tnzapi.base import MessageResult

class SMS(Common):
    
    FromNumber      = ""
    SMSEmailReply   = ""
    ForceGSMChars	= False
    MessageText     = ""

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgs(kwargs)

    """ Update Data """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "FromNumber":
                self.FromNumber = value

            if key == "SMSEmailReply":
                self.SMSEmailReply = value

            if key == "ForceGSMChars":
                self.ForceGSMChars = value
            
            if key == "MessageText":
                self.MessageText = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "SMS",
            "APIVersion": self.APIVersion,
            "MessageID" : self.MessageID,
            "MessageData" :
            {
                "Mode": self.SendMode,
                "Reference": self.Reference,
                "SendTime": self.SendTime,
                "TimeZone": self.Timezone,
                "SubAccount": self.SubAccount,
                "Department": self.Department,
                "ChargeCode": self.ChargeCode,
                "FromNumber": self.FromNumber,
                "SMSEmailReply": self.SMSEmailReply,
                "ForceGSMChars": self.ForceGSMChars,
                "Message": self.MessageText,
                "Destinations" : self.Recipients,
                "Files": self.Attachments
            }
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL, data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return MessageResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return MessageResult(error=str(e))
            
        return MessageResult(response=r)

    """ Function to send message """
    def SendMessage(self, **kwargs):

        self.SetArgs(kwargs)

        if not self.Sender :
            return MessageResult(error="Empty Sender")
        
        if not self.APIKey :
            return MessageResult(error="Empty API Key")
        
        if not self.MessageText:
            return MessageResult(error="Emtpy Message Text")

        if not self.Recipients:
            return MessageResult(error="Empty recipient(s)")

        return self.__PostMessage()

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'SMS(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'