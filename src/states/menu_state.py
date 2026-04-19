from pygame import Surface, Event, MOUSEBUTTONDOWN, draw, SRCALPHA, Rect, transform, display
from src.core.state import State
from src.utils.ui import Button, Label
from src.utils.image_manager import image_manager
from src.utils.platform import get_platform
from src.utils.video_driver import get_video_driver
import pygame

class MenuState(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.buttons = []
        self.title = None
        self.info = None
        self.background_image = None
        self.background_color = (20, 10, 60)
        self.screen_width = 0
        self.screen_height = 0
    
    def _get_responsive_values(self, width, height):
        panel_width = max(200, int(width * 0.19))
        button_width = max(150, int(width * 0.185))
        button_height = max(40, int(height * 0.085))
        title_font_size = max(24, int(height * 0.068))
        button_font_size = max(12, int(height * 0.025))
        info_font_size = max(10, int(height * 0.02))
        button_spacing = max(60, int(height * 0.11))
        button_start_y = max(100, int(height * 0.256))
        title_y = int(height * 0.07)
        
        return {
            'panel_width': panel_width,
            'button_width': button_width,
            'button_height': button_height,
            'title_font_size': title_font_size,
            'button_font_size': button_font_size,
            'info_font_size': info_font_size,
            'button_spacing': button_spacing,
            'button_start_y': button_start_y,
            'title_y': title_y,
            'button_x': int(panel_width * 0.15)
        }
    
    def _init_ui(self):
        pass
    
    def _create_ui(self, width, height):
        self.buttons.clear()
        values = self._get_responsive_values(width, height)
        
        self.title = Label(
            int(width / 2) + 220, values['title_y'],
            text='Project Mars',
            font_size=values['title_font_size'],
            text_color=(255, 255, 255),
            bg_color=(0, 0, 0, 0),
            font_name="exo2.ttf",
            centered=True
        )
        
        info_text = f"Driver: {get_video_driver(display)} \n                                OS: {get_platform()}"
        self.info = Label(
            width - 20, height - 20,
            text=info_text,
            font_size=values['info_font_size'],
            text_color=(200, 200, 200),
            bg_color=(0, 0, 0),
            font_name="exo2.ttf",
            centered=False
        )
        self.info.x = width - self.info.rect.width - 20
        self.info.y = height - self.info.rect.height - 20

        buttons_data = [
            ("Play", self._on_play_clicked),
            ("Settings", self._on_settings_clicked),
            ("About", self._on_about_clicked)
        ]
        
        for i, (text, callback) in enumerate(buttons_data):
            y = values['button_start_y'] + (i * values['button_spacing'])
            btn = Button(
                values['button_x'], y,
                values['button_width'], values['button_height'],
                text=text,
                font_size=values['button_font_size'],
                bg_color=(0, 0, 0),
                border_radius=2,
                text_color=(255, 255, 255),
                text_scaled=True,
                font_name="exo2.ttf",
                bg_alpha=100
            )
            btn.on_hover(bg_color=(255, 255, 255), bg_alpha=10)
            btn.on_click(callback)
            self.buttons.append(btn)
    
    def _on_play_clicked(self):
        print("ГРАТИ натнуто")
    
    def _on_settings_clicked(self):
        print("НАЛАШТУВАННЯ натнуто")
    
    def _on_scores_clicked(self):
        print("РЕКОРДИ натнуто")
    
    def _on_about_clicked(self):
        print("ПРО ГУРУ натнуто")
    
    def _on_exit_clicked(self):
        import pygame
        pygame.quit()
        exit()
    
    def _load_background_image(self, image_path):
        if self.screen_width > 0 and self.screen_height > 0:
            self.background_image = image_manager.load_image(image_path, self.screen_width, self.screen_height, cache=False)
        else:
            self.background_image = None
    
    def _draw_gradient_background(self, screen):
        gradient = image_manager.create_gradient_surface(
            screen.get_width(),
            screen.get_height(),
            color1=(80, 40, 160), 
            color2=(20, 10, 40), 
            direction='vertical'
        )
        screen.blit(gradient, (0, 0))
    
    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    btn.handle_event(e)
    
    def update(self, dt):
        for btn in self.buttons:
            btn.update()
    
    def draw(self, screen):
        width, height = screen.get_size()
        
        if width != self.screen_width or height != self.screen_height:
            self.screen_width = width
            self.screen_height = height
            self._create_ui(width, height)
            self._load_background_image('menu_bg.jpg')
        
        if self.background_image:
            bg_scaled = transform.scale(self.background_image, (width, height))
            screen.blit(bg_scaled, (0, 0))
        else:
            self._draw_gradient_background(screen)
        
        values = self._get_responsive_values(width, height)
        panel_width = values['panel_width']
        panel_surface = Surface((panel_width, height), SRCALPHA)
        panel_surface.fill(((10, 10, 10, 10)))
        screen.blit(panel_surface, (0, 0))
        
        self.title.draw(screen)
        self.info.draw(screen)
        
        for btn in self.buttons:
            btn.draw(screen)