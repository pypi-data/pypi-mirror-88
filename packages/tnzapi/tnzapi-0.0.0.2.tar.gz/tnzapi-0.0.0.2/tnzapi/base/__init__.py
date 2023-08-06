""" reference to tnzapi.base.functions """
def Functions():

    from tnzapi.base.functions import Functions as functions

    return functions()

""" Reference to tnzapi.base.get.message_result.MessageResult """
def MessageResult(**kwargs):

    from tnzapi.base.send.message_result import MessageResult as message_result

    return message_result(**kwargs)

""" Reference to tnzapi.base.get.status_request_result.StatusRequestResult """
def StatusRequestResult(**kwargs):

    from tnzapi.base.get.status_request_result import StatusRequestResult as status_request_result

    return status_request_result(**kwargs)

""" Reference to tnzapi.base.get.result_request_result.ResultRequestResult """
def ResultRequestResult(**kwargs):

    from tnzapi.base.get.result_request_result import ResultRequestResult as result_request_result

    return result_request_result(**kwargs)

""" Reference to tnzapi.base.get.sms_received_result.SMSReceivedResult """
def SMSReceivedResult(**kwargs):

    from tnzapi.base.get.sms_received_result import SMSReceivedResult as sms_received_result

    return sms_received_result(**kwargs)

""" Reference to tnzapi.base.get.inbound_sms_result.InboundSMSResult """
def InboundSMSResult(**kwargs):

    from tnzapi.base.get.inbound_sms_result import InboundSMSResult as inbound_sms_result

    return inbound_sms_result(**kwargs)

""" Reference to tnzapi.base.set.set_request_result.SetRequestResult """
def SetRequestResult(**kwargs):

    from tnzapi.base.set.set_request_result import SetRequestResult as set_request_result

    return set_request_result(**kwargs)

""" Reference to tnzapi.base.get.keypad.Keypad """
def Keypad(**kwargs):

    from tnzapi.base.send.keypad import Keypad as keypad

    return keypad(**kwargs)