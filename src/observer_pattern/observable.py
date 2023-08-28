class Observable(object):
    def __init__(self):
        self.observers = []

    def add_observer(self, new_observer):
        self.observers.append(new_observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)