from src.utils.video_driver import *
from src.utils.ui import *
from src.utils.platform import get_platform
from src.core.state_manager import StateManager
from src.states import MenuState

from pygame import *
from tkinter import messagebox

WIDTH, HEIGHT = 1280, 700
FPS = 60
BG_COLOR = (60, 30, 155)

class Window:
    def __init__(self):
        pre_init_driver()
        init()
        self.platform = get_platform()
        if not self.platform.startswith("GNU/Linux"):
            messagebox.showwarning("Warning", "Ця гра працює тільки на GNU/Linux\nНа інших платформах вона може працювати не стабільно")

        self.screen = display.set_mode(
            (WIDTH, HEIGHT), 
            DOUBLEBUF | RESIZABLE | HWSURFACE
        )
        
        self.driver = get_video_driver(display)
        self.clock = time.Clock()
        self.running = True
        
        self.state_manager = StateManager()
        self._init_states()
        
        print(f"Active driver: {self.driver}, Platform: {self.platform}")

    def _init_states(self):
        menu_state = MenuState(self.state_manager)
        self.state_manager.add_state("menu", menu_state)
        self.state_manager.set_state("menu")

    def handle_events(self):
        events_list = event.get()
        for e in events_list:
            if e.type == QUIT:
                self.running = False
        
        self.state_manager.handle_events(events_list)

    def update(self):
        dt = self.clock.get_time() / 1000.0
        self.state_manager.update(dt)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.state_manager.draw(self.screen)
        display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        quit()

if __name__ == "__main__":
    win = Window()
    win.run()