from view.event import Event

class View(object):
    OnViewUpdated = Event()
     
    def __init__(self):
        self.OnViewUpdated = Event()
         
    def ViewUpdated(self):
        # This function will be executed once a lock is broken and will
        # raise an event
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod