from pygame import Surface
from pygame.event import Event

class State:
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events: list[Event]):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: Surface):
        pass
