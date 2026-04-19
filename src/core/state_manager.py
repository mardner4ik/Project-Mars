from pygame import Surface
from pygame.event import Event
from src.core.state import State

class StateManager:
    def __init__(self):
        self.states: dict[str, State] = {}
        self.active_state: State = None

    def add_state(self, name: str, state: State):
        self.states[name] = state

    def set_state(self, name: str):
        if name in self.states:
            self.active_state = self.states[name]

    def handle_events(self, events: list[Event]):
        if self.active_state:
            self.active_state.handle_events(events)

    def update(self, dt: float):
        if self.active_state:
            self.active_state.update(dt)

    def draw(self, screen: Surface):
        if self.active_state:
            self.active_state.draw(screen)
