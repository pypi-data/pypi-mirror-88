import json
import requests

from tnzapi.base.functions import Functions

class ResultRequestResult(object):

    def __init__(self, **kwargs):

        self.Destinations = []
        
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

            if response["Data"]:
                for key in response["Data"]:
                    if key == "MessageID":
                        self.MessageID = response["Data"][key]
                    if key == "Status" or key == "Location":
                        self.Status = response["Data"][key]
                    if key == "JobNum":
                        self.JobNum = response["Data"][key]
                    if key == "Account":
                        self.Account = response["Data"][key]
                    if key == "SubAccount":
                        self.SubAccount = response["Data"][key]
                    if key == "Department":
                        self.Department = response["Data"][key]
                    if key == "Count":
                        self.Count = response["Data"][key]
                    if key == "Complete":
                        self.Complete = response["Data"][key]
                    if key == "Success":
                        self.Success = response["Data"][key]
                    if key == "Failed":
                        self.Failed = response["Data"][key]
                    if key == "Destinations":
                        for destination in response["Data"][key]:
                            self.Destinations.append(destination)
                    if key == "Message":
                        self.Message = response["Data"][key]
                
    
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
                    "Count": self.Count,
                    "Complete": self.Complete,
                    "Success": self.Success,
                    "Failed": self.Failed,
                    "Destinations": self.Destinations
                }
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

    """ Getters/Setters """
    @property
    def Result(self):
        return self.__result

    @Result.setter
    def Result(self,val):
        self.__result = val

    @property
    def MessageID(self):
        return self.__messageid
    
    @MessageID.setter
    def MessageID(self,val):
        self.__messageid = val

    @property
    def Status(self):
        return self.__status
    
    @Status.setter
    def Status(self,val):
        self.__status = val
    
    @property
    def JobNum(self):
        return self.__jobnum
    
    @JobNum.setter
    def JobNum(self,val):
        self.__jobnum = val
    
    @property
    def Account(self):
        return self.__account
    
    @Account.setter
    def Account(self,val):
        self.__account = val
    
    @property
    def SubAccount(self):
        return self.__subaccount
    
    @SubAccount.setter
    def SubAccount(self,val):
        self.__subaccount = val
    
    @property
    def Department(self):
        return self.__department
    
    @Department.setter
    def Department(self,val):
        self.__department = val
    
    @property
    def Count(self):
        return self.__count
    
    @Count.setter
    def Count(self,val):
        self.__count = val

    @property
    def Complete(self):
        return self.__complete
    
    @Complete.setter
    def Complete(self,val):
        self.__complete = val
    
    @property
    def Success(self):
        return self.__success
    
    @Success.setter
    def Success(self,val):
        self.__success = val
    
    @property
    def Failed(self):
        return self.__failed
    
    @Failed.setter
    def Failed(self,val):
        self.__failed = val

    @property
    def Destinations(self):
        return self.__destinations
    
    @Destinations.setter
    def Destinations(self, destination):
        self.__destinations = destination

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'def StatusRequestResult()'

class ResultRequestDestination(object):

    DestSeq     = ""
    Destination = ""
    Type        = "Unknown"
    Status      = "Unknown"
    Result      = "Unknown"
    SentDate    = ""

    def __init__(self, destination):

        if destination["DestSeq"]:
            self.DestSeq = destination["DestSeq"]
        
        if destination["Destination"]:
            self.Destination = destination["Destination"]
        
        if destination["Type"]:
            self.Type = destination["Type"]
        
        if destination["Status"]:
            self.Status = destination["Status"]
        
        if destination["Result"]:
            self.Result = destination["Result"]
        
        if destination["SentDate"]:
            self.SentDate = destination["SentDate"]
        