class Get(object):

    def __init__(self):
        self._status = None
        self._inboundsms = None
        self._smsreceived = None
        self._result = None

    def Status(self,**kwargs):

        if self._status == None:
            from tnzapi.get.status import Status
            self._status = Status(kwargs)

        return self._status
    
    def InboundSMS(self,**kwargs):

        if self._inboundsms == None:
            from tnzapi.get.inbound_sms import InboundSMS
            self._inboundsms = InboundSMS(kwargs)

        return self._inboundsms

    def SMSReceived(self, **kwargs):

        if self._smsreceived == None:
            from tnzapi.get.sms_received import SMSReceived
            self._smsreceived = SMSReceived(kwargs)

        return self._smsreceived
    
    def Result(self, **kwargs):

        if self._result == None:
            from tnzapi.get.result import Result
            self._result = Result(kwargs)

        return self._result