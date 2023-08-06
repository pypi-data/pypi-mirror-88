import json
import requests

from tnzapi.base.functions import Functions

class SMSReceivedResult(object):

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

            #print(r.text)

            response = Functions.__parsejson__(self,r.text)

            if response["Result"]:
                self.Result = response["Result"]

            if self.Result == "Success":

                for key in response["Data"]:
                    if key == "MessageID":
                        self.MessageID = response["Data"][key]
                    if key == "Status":
                        self.Status = response["Data"][key]
                    if key == "JobNum":
                        self.JobNum = response["Data"][key]
                    if key == "Account":
                        self.Account = response["Data"][key]
                    if key == "SubAccount":
                        self.SubAccount = response["Data"][key]
                    if key == "Department":
                        self.Department = response["Data"][key]
                    if key == "MessageSent":
                        self.MessageSent = MessageSent(response["Data"][key])
                    if key == "MessageReceived":
                        for message in response["Data"][key]:
                            self.MessageReceived.append(message)

            else:
                if "Message" in response:
                    self.Message = response["Message"]
                else:
                    self.Message = ""

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":

            return {
                "Result": self.Result,
                "Data": {
                    "MessageID": self.MessageID,
                    "Status": self.Status,
                    "JobNum": self.JobNum,
                    "Account": self.Account,
                    "SubAccount": self.SubAccount,
                    "Department": self.Department,
                    "MessageSent": {
                        "Date": self.MessageSent.Date,
                        "Destination": self.MessageSent.Destination,
                        "MessageText": self.MessageSent.MessageText
                    },
                    "MessageReceived": self.MessageReceived
                }
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

class MessageSent(object):

    def __init__(self, message):

        if message["Date"]:
            self.Date = message["Date"]
        
        if message["Destination"]:
            self.Destination = message["Destination"]
        
        if message["MessageText"]:
            self.MessageText = message["MessageText"]
