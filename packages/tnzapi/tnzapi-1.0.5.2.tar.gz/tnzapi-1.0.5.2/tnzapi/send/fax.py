import requests
import json

from tnzapi.send._common import Common
from tnzapi.base import MessageResult

class Fax(Common):

    Resolution          = "high"
    CSID                = ""
    StampFormat		    = ""
    WatermarkFolder     = ""
    WatermarkFirstPage  = "No"
    WatermarkAllPages   = "No"
    RetryAttempts	    = 0
    RetryPeriod		    = 0

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

    """ Update Data """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "Resolution":
                self.Resolution = value
            
            if key == "CSID":
                self.CSID = value
            
            if key == "StampFormat":
                self.StampFormat = value
            
            if key == "WatermarkFolder":
                self.WatermarkFolder = value
            
            if key == "WatermarkFirstPage":
                self.WatermarkFirstPage = value
            
            if key == "WatermarkAllPages":
                self.WatermarkAllPages = value
            
            if key == "RetryAttempts":
                self.RetryAttempts = value
            
            if key == "RetryPeriod":
                self.RetryPeriod = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "Fax",
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
                "Resolution": self.Resolution,
                "CSID": self.CSID,
                "StampFormat": self.StampFormat,
                "WatermarkFolder": self.WatermarkFolder,
                "WatermarkFirstPage": self.WatermarkFirstPage,
                "WatermarkAllPages": self.WatermarkAllPages,
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
            return MessageResult(error="Empty APIKey")
        
        if not self.Recipients:
            return MessageResult(error="Empty Recipient(s)")

        if not self.Attachments:
            return MessageResult(error="Empty Attachment(s)")

        return self.__PostMessage()

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Fax(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'