from pygame import MOUSEBUTTONDOWN
from src.core.state import State
from src.utils.ui import Button, ScrollingFrame


class SavesState(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.buttons = []
        self.scrolling_frame = None
        self.screen_width = 0
        self.screen_height = 0

    def _create_ui(self, width, height):
        self.buttons.clear()
        
        frame_w = int(width * 0.6)
        frame_h = int(height * 0.6)
        frame_x = int((width - frame_w) / 2)
        frame_y = int(height * 0.1)
        
        self.scrolling_frame = ScrollingFrame(
            frame_x, frame_y, frame_w, frame_h,
            bg_color=(30, 30, 40), bg_alpha=180, border_radius=8
        )
        
        for i in range(15):
            btn = Button(
                20, 20 + i * 70,
                frame_w - 40, 60,
                text=f"Save Slot {i+1}",
                font_size=24,
                bg_color=(50, 50, 60),
                text_color=(220, 220, 220),
                border_radius=5
            )
            btn.on_hover(bg_color=(80, 80, 90))
            btn.on_click(lambda idx=i: print(f"Loaded slot {idx+1}"))
            self.scrolling_frame.add_element(btn)
            
        btn_w = 200
        btn_h = 50
        btn_spacing = 40
        
        total_btns_w = (btn_w * 2) + btn_spacing
        start_x = (width - total_btns_w) // 2
        btn_y = frame_y + frame_h + int(height * 0.08)
        
        new_game_btn = Button(
            start_x, btn_y, btn_w, btn_h,
            text="New Game", font_size=22,
            bg_color=(40, 120, 60), text_color=(255, 255, 255), border_radius=5
        )
        new_game_btn.on_hover(bg_color=(60, 150, 80))
        new_game_btn.on_click(self._on_new_game)
        
        exit_btn = Button(
            start_x + btn_w + btn_spacing, btn_y, btn_w, btn_h,
            text="Exit", font_size=22,
            bg_color=(150, 50, 50), text_color=(255, 255, 255), border_radius=5
        )
        exit_btn.on_hover(bg_color=(180, 70, 70))
        exit_btn.on_click(self._on_exit)
        
        self.buttons.extend([new_game_btn, exit_btn])

    def _on_new_game(self):
        print("Start New Game")
        
    def _on_exit(self):
        print("Exit Saves")

    def handle_events(self, events):
        for e in events:
            if self.scrolling_frame:
                self.scrolling_frame.handle_event(e)
            if e.type == MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    btn.handle_event(e)

    def update(self, dt):
        if self.scrolling_frame:
            self.scrolling_frame.update()
        for btn in self.buttons:
            btn.update()

    def draw(self, screen):
        width, height = screen.get_size()
        if width != self.screen_width or height != self.screen_height:
            self.screen_width = width
            self.screen_height = height
            self._create_ui(width, height)
            
        screen.fill((15, 15, 25))
        
        if self.scrolling_frame:
            self.scrolling_frame.draw(screen)
        for btn in self.buttons:
            btn.draw(screen)