import requests
import json

from tnzapi.send._common import Common
from tnzapi.base import MessageResult

class Email(Common):

    EmailSubject    = ""
    MessagePlain    = ""
    MessageHTML     = ""

    SMTPFrom        = ""
    From            = ""
    FromEmail       = ""
    ReplyTo         = ""

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgs(kwargs)
    
    """ Set Args """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "EmailSubject":
                self.EmailSubject = value
            
            if key == "MessagePlain":
                self.MessagePlain = value
            
            if key == "MessageHTML":
                self.MessageHTML = value

            if key == "SMTPFrom":
                self.SMTPFrom = value

            if key == "From":
                self.From = value
            
            if key == "FromEmail":
                self.FromEmail = value
            
            if key == "ReplyTo":
                self.ReplyTo = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "Email",
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
                "EmailSubject": self.EmailSubject,
                "SMTPFrom": self.SMTPFrom,
                "From": self.From,
                "FromEmail": self.FromEmail,
                "ReplyTo": self.ReplyTo,
                "MessagePlain": self.MessagePlain,
                "MessageHTML": self.MessageHTML,
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

        if not self.MessagePlain and not self.MessageHTML:
            return MessageResult(error="Missing MessagePlain and MessageHTML")

        if not self.Recipients:
            return MessageResult(error="Missing Recipient(s)")

        return self.__PostMessage()

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Email(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'
    