class Set(object):

    def __init__(self):
        self._abort = None
        self._pacing = None
        self._reschedule = None
        self._resubmit = None

    def Abort(self,**kwargs):

        if self._abort == None:
            from tnzapi.set.abort import Abort
            self._abort = Abort(kwargs)

        return self._abort
    
    def Pacing(self,**kwargs):

        if self._pacing == None:
            from tnzapi.set.pacing import Pacing
            self._pacing = Pacing(kwargs)

        return self._pacing

    def Reschedule(self,**kwargs):

        if self._reschedule == None:
            from tnzapi.set.reschedule import Reschedule
            self._reschedule = Reschedule(kwargs)
        
        return self._reschedule

    def Resubmit(self,**kwargs):

        if self._resubmit == None:
            from tnzapi.set.resubmit import Resubmit
            self._resubmit = Resubmit(kwargs)

        return self._resubmit