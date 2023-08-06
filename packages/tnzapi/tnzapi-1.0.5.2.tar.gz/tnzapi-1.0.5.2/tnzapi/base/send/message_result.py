import json

from tnzapi.base.functions import Functions

class MessageResult(object):

    def __init__(self, **kwargs):

        self.Result = ""
        self.MessageID = ""
        self.Message = ""

        for key, value in kwargs.items():
            
            if key == "response":
                print(key)
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.Message = value

    def ParseResponse(self, r):

        if r.text:

            self.__response_string__ = r.text

            response = Functions.__parsejson__(self,r.text)

            for key in response:

                if key == "Result":
                    self.Result = response[key]
                
                if key == "MessageID":
                    self.MessageID = response[key]
                
                if key == "Message":
                    self.Message = response[key]

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":
            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
            }

        if self.Result == "Failed":
            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
                "Message": self.Message
            }
        
        return {
            "Result": self.Result,
            "Message": self.Message
        }
    
    @property
    def Result(self):
        return self.__Result
    
    @Result.setter
    def Result(self,val):
        self.__Result = val

    @property
    def MessageID(self):
        return self.__MessageID
    
    @MessageID.setter
    def MessageID(self,val):
        self.__MessageID = val
    
    @property
    def Message(self):
        return self.__Message
    
    @Message.setter
    def Message(self,val):
        self.__Message = val

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'MessageResult('+ self.__response_string__ +')'

    