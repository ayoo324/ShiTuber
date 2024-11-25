from Helpers.Singleton import Singleton
eventQueue = {}
subscribers = {}
eventReceiptMap = {}
@Singleton
class EventQueue:
    def addToEventQueue(eventId, event):
        if eventId not in eventQueue:
            eventQueue[eventId] = []
        eventQueue[eventId].append(event)

    def subscribeToEvent(identifier, eventId):
        if identifier not in subscribers:
            subscribers[identifier] = set()
        subscribers[identifier].add(eventId)
        
    def unsubscribeFromEvent(identifier, eventId):
        if identifier not in subscribers:
            pass
        subscribers[identifier].remove(eventId)

    def getEvents(identifier):
        if identifier not in subscribers:
            pass 
        