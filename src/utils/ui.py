import os
from pygame import *

init()

CURSORS = {
    "arrow": SYSTEM_CURSOR_ARROW,
    "hand": SYSTEM_CURSOR_HAND,
    "ibeam": SYSTEM_CURSOR_IBEAM,
    "wait": SYSTEM_CURSOR_WAIT,
    "crosshair": SYSTEM_CURSOR_CROSSHAIR,
    "no": SYSTEM_CURSOR_NO,
    "size_all": SYSTEM_CURSOR_SIZEALL,
    "size_nesw": SYSTEM_CURSOR_SIZENESW,
    "size_ns": SYSTEM_CURSOR_SIZENS,
    "size_nwse": SYSTEM_CURSOR_SIZENWSE,
    "size_we": SYSTEM_CURSOR_SIZEWE
}

FONTS_PATH = "src/assets/fonts"

def get_font(name, size):
    if name is None:
        return font.SysFont(None, size)
    
    full_path = os.path.join(FONTS_PATH, name)
    if os.path.exists(full_path):
        return font.Font(full_path, size)
    return font.SysFont(name, size)

class UIElement:
    def __init__(self, x, y, width, height, bg_color=(255, 255, 255), border_radius=0, alpha=255, centered=False):
        self._width = width
        self._height = height
        self.bg_color = bg_color
        self.border_radius = border_radius
        self.alpha = alpha
        self.centered = centered
        self.visible = True
        
        self.rect = Rect(0, 0, width, height)
        self.surface = Surface((width, height), SRCALPHA)
        self.set_position(x, y)

    def set_position(self, x, y):
        if self.centered:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def set_size(self, width, height):
        curr_pos = self.rect.center if self.centered else self.rect.topleft
        self._width, self._height = width, height
        self.rect.size = (width, height)
        self.surface = Surface((width, height), SRCALPHA)
        self.set_position(*curr_pos)

    @property
    def x(self): return self.rect.centerx if self.centered else self.rect.x
    @x.setter
    def x(self, value):
        if self.centered: self.rect.centerx = value
        else: self.rect.x = value

    @property
    def y(self): return self.rect.centery if self.centered else self.rect.y
    @y.setter
    def y(self, value):
        if self.centered: self.rect.centery = value
        else: self.rect.y = value

    def _render_shape(self):
        self.surface.fill((0, 0, 0, 0))
        color = self.bg_color
        render_color = (*color[:3], self.alpha)
        draw.rect(self.surface, render_color, (0, 0, self.rect.width, self.rect.height), border_radius=self.border_radius)

    def draw(self, screen):
        if self.visible:
            self._render_shape()
            screen.blit(self.surface, self.rect.topleft)

class Label(UIElement):
    def __init__(self, x, y, text='', font_size=24, text_color=(0, 0, 0), font_name=None, **kwargs):
        self.font_name = font_name
        self.font_size = font_size
        self.font = get_font(font_name, font_size)
        self.text = text
        self.text_color = text_color
        
        tmp_surf = self.font.render(self.text, True, self.text_color)
        width = kwargs.pop('width', tmp_surf.get_width())
        height = kwargs.pop('height', tmp_surf.get_height())
        
        super().__init__(x, y, width, height, **kwargs)

    def set_text(self, text):
        self.text = text

    def draw(self, screen):
        if not self.visible: return
        self._render_shape()
        text_surf = self.font.render(self.text, True, self.text_color)
        text_surf.set_alpha(self.alpha)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.surface.blit(text_surf, text_rect)
        screen.blit(self.surface, self.rect.topleft)

class Button(UIElement):
    def __init__(self, x, y, width, height, text='', font_size=24, font_name=None, **kwargs):
        self.bg_alpha = kwargs.pop('bg_alpha', 255)
        self.text_alpha = kwargs.pop('text_alpha', 255)
        self.text_color = kwargs.pop('text_color', (0, 0, 0))
        self.cursor_on_hover = kwargs.pop('cursor_on_hover', CURSORS["hand"])
        self.blocked = kwargs.pop('blocked', False)
        self.text_scaled = kwargs.pop('text_scaled', False)

        super().__init__(x, y, width, height, alpha=self.bg_alpha, **kwargs)
        
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font = get_font(font_name, font_size)
        self.callback = None
        self.hover_callback = None
        self.is_hovered = False

        self._normal_state = {
            'bg_color': self.bg_color,
            'bg_alpha': self.bg_alpha,
            'text_color': self.text_color,
            'text_alpha': self.text_alpha,
            'text': self.text
        }
        self._hover_state = self._normal_state.copy()

    def on_click(self, callback):
        self.callback = callback

    def on_hover(self, **kwargs):
        if 'cursor' in kwargs:
            self.cursor_on_hover = kwargs.pop('cursor')
        self._hover_state.update(kwargs)

    def update(self):
        if not self.visible:
            self.is_hovered = False
            return
        
        mouse_pos = mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered:
            if self.blocked:
                mouse.set_cursor(CURSORS["no"])
            else:
                mouse.set_cursor(self.cursor_on_hover)
            state = self._hover_state
            if not was_hovered and self.hover_callback:
                self.hover_callback()
        else:
            state = self._normal_state
            if was_hovered:
                mouse.set_cursor(CURSORS["arrow"])

        self.bg_color = state['bg_color']
        self.alpha = state['bg_alpha']
        self.text_color = state['text_color']
        self.text_alpha = state['text_alpha']
        self.text = state['text']

    def handle_event(self, event):
        if not self.visible or not self.is_hovered or self.blocked:
            return
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.callback:
                self.callback()

    def draw(self, screen):
        if not self.visible: return
        self._render_shape()
        
        text_surf = self.font.render(self.text, True, self.text_color)
        
        if self.text_scaled:
            tw, th = text_surf.get_size()
            ratio = min(self.rect.width / tw, self.rect.height / th)
            new_size = (int(tw * ratio), int(th * ratio))
            text_surf = transform.smoothscale(text_surf, new_size)
            
        text_surf.set_alpha(self.text_alpha)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.surface.blit(text_surf, text_rect)
        screen.blit(self.surface, self.rect.topleft)