import json
import requests

from tnzapi.base.functions import Functions

class InboundSMSResult(object):

    def __init__(self,**kwargs):

        self.MessageReceived = []

        for key, value in kwargs.items():
            
            if key == "response":
                print(key)
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.Message = value

    def ParseResponse(self, r):

        if r.text:

            response = Functions.__parsejson__(self,r.text)

            if response["Result"]:
                self.Result = response["Result"]

            if self.Result == "Success":
                if response["Data"]["MessageReceived"]:
                    for key in response["Data"]["MessageReceived"]:
                        self.MessageReceived.append(key)
            else:
                self.Message = response["Message"]

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":
            return {
                "Result": self.Result,
                "MessageReceived": self.MessageReceived
            }

        if self.Result == "Failed":
            return {
                "Result": self.Result,
                "Message": self.Message
            }
        
        return {
            "Result": self.Result,
            "Message": self.Message
        }

    """ Getters/Setters """
    @property
    def Result(self):
        return self.__result

    @Result.setter
    def Result(self,val):
        self.__result = val
    
    @property
    def MessageReceived(self):
        return self.__messagereceived
    
    @MessageReceived.setter
    def MessageReceived(self, message):
        self.__messagereceived = message

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'InboundSMSResult()'

class InboundSMSMessage(object):

    def __init__(self, received):

        if received["Date"]:
            self.Date = received["Date"]
        
        if received["From"]:
            self.From = received["From"]
        
        if received["MessageText"]:
            self.MessageText = received["MessageText"]
