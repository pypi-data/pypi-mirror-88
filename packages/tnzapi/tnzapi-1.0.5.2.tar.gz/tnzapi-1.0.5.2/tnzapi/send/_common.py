#from tnzapi import __Sender__, __APIKey__, __APIVersion__, __APIURL__

from tnzapi import _config
from tnzapi.base.functions import Functions

class Common:

    Sender          = _config.__Sender__
    APIKey          = _config.__APIKey__
    APIVersion      = _config.__APIVersion__
    APIURL          = _config.__APIURL__ + "/send/"
    APIHeaders      = _config.__APIHeaders__

    MessageID       = ""
    
    Reference       = ""
    SendTime        = ""
    Timezone        = "New Zealand"
    SubAccount      = ""
    Department      = ""
    ChargeCode      = ""

    Attachments     = []
    Recipients      = []

    SendMode        = ""

    """ Constructor """
    def __init__(self,kwargs):

        self.SetArgs(kwargs)

    """ Set Args """
    def SetArgs(self, kwargs):

        #print("SetArgs()")

        if "Sender" in kwargs:
            self.Sender = _config.__Sender__ = kwargs.pop("Sender")

        if "APIKey" in kwargs:
            self.APIKey = _config.__APIKey__ = kwargs.pop("APIKey")
        
        if "MessageID" in kwargs:
            self.MessageID = kwargs.pop("MessageID")

        if "Reference" in kwargs:
            self.Reference = kwargs.pop("Reference")
        
        if "SendTime" in kwargs:
            self.SendTime = kwargs.pop("SendTime")

        if "Timezone" in kwargs:
            self.Timezone = kwargs.pop("Timezone")
        
        if "SubAccount" in kwargs:
            self.SubAccount = kwargs.pop("SubAccount")

        if "Department" in kwargs:
            self.Department = kwargs.pop("Department")
        
        if "ChargeCode" in kwargs:
            self.ChargeCode = kwargs.pop("ChargeCode")

        if "Recipients" in kwargs:
            self.AddRecipient(kwargs.pop("Recipients"))

        if "Attachments" in kwargs:
            self.AddAttachment(kwargs.pop("Attachments"))
        
        if "SendMode" in kwargs:
            self.SendMode = kwargs.pop("SendMode")

    """ Add Recipient """
    def AddRecipient(self, recipient):

        if recipient:

            #print(isinstance(recipient,dict))

            if isinstance(recipient,str):

                dest = {
                    "Recipient": recipient
                }

                self.Recipients.append(dest)

            if isinstance(recipient, (list, tuple)):

                for key in recipient:
                    
                    dest = {
                        "Recipient": key
                    }

                    self.Recipients.append(dest)

            if isinstance(recipient,dict):

                self.Recipients.append(recipient)
            

    """ Add Attachment """
    def AddAttachment(self, attachment):

        if attachment:
            if isinstance(attachment,str):

                file = {
                    "Name": self.__getfilename__(attachment),
                    "Data": self.__getfilecontent__(attachment)
                }

                self.Attachments.append(file)

            if isinstance(attachment, (list, tuple)):

                for key in attachment:

                    file = {
                        "Name": self.__getfilename__(key),
                        "Data": self.__getfilecontent__(key)
                    }

                    self.Attachments.append(file)

    def __getfilename__(self,filename):

        return Functions.__getfilename__(self, filename)

    def __getfilecontent__(self,filename):
        return Functions.__getfilecontents__(self, filename)
    
    def __pretty__(self,obj):

        return Functions.__pretty__(self,obj)