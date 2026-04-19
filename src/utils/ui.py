import os
from pygame import *
from pygame import scrap

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
        
        if self.text_scaled:
            target_h = int(self.rect.height * 0.8)
            temp_font = get_font(self.font_name, target_h)
            text_surf = temp_font.render(self.text, True, self.text_color)
            if text_surf.get_width() > self.rect.width * 0.9:
                target_h = int(target_h * (self.rect.width * 0.9 / text_surf.get_width()))
                temp_font = get_font(self.font_name, max(1, target_h))
                text_surf = temp_font.render(self.text, True, self.text_color)
        else:
            text_surf = self.font.render(self.text, True, self.text_color)
            
        text_surf.set_alpha(self.text_alpha)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.surface.blit(text_surf, text_rect)
        screen.blit(self.surface, self.rect.topleft)

class InputArea(UIElement):
    def __init__(self, x, y, width, height, font_size=24, font_name=None, **kwargs):
        self.bg_alpha = kwargs.pop('bg_alpha', 255)
        self.text_color = kwargs.pop('text_color', (0, 0, 0))
        self.placeholder_text = kwargs.pop('placeholder_text', '')
        self.placeholder_text_color = kwargs.pop('placeholder_text_color', (150, 150, 150))
        self.password_char = kwargs.pop('password_char', None)
        self.max_length = kwargs.pop('max_length', None)
        self.border_color = kwargs.pop('border_color', (200, 200, 200))
        self.focused_border_color = kwargs.pop('focused_border_color', (0, 120, 255))
        self.border_width = kwargs.pop('border_width', 2)
        self.selection_color = kwargs.pop('selection_color', (0, 120, 255, 100))
        self.cursor_color = kwargs.pop('cursor_color', (0, 0, 0))
        
        super().__init__(x, y, width, height, alpha=self.bg_alpha, **kwargs)
        
        self.font_name = font_name
        self.font_size = font_size
        self.font = get_font(font_name, font_size)
        
        self.text = ""
        self.is_focused = False
        self.cursor_pos = 0
        self.selection_start = 0
        self.scroll_x = 0
        
        self.cursor_visible = True
        self.last_blink = time.get_ticks()
        self.is_hovered = False
        self.is_dragging = False
        self.padding_x = 8
        
        try:
            scrap.init()
        except:
            pass

    def _get_display_text(self):
        if self.password_char:
            return self.password_char * len(self.text)
        return self.text

    def _get_index_from_mouse(self, mouse_pos):
        rel_x = mouse_pos[0] - self.rect.x - self.padding_x + self.scroll_x
        disp = self._get_display_text()
        for i in range(len(disp) + 1):
            w = self.font.size(disp[:i])[0]
            if w > rel_x:
                if i > 0 and rel_x < (self.font.size(disp[:i-1])[0] + w) / 2:
                    return i - 1
                return i
        return len(disp)

    def _adjust_scroll(self):
        disp = self._get_display_text()
        cursor_x = self.font.size(disp[:self.cursor_pos])[0]
        max_scroll = max(0, self.font.size(disp)[0] - (self.rect.width - 2 * self.padding_x))
        if cursor_x - self.scroll_x < 0:
            self.scroll_x = max(0, cursor_x - 10)
        elif cursor_x - self.scroll_x > self.rect.width - 2 * self.padding_x:
            self.scroll_x = min(max_scroll, cursor_x - self.rect.width + 2 * self.padding_x + 10)
        self.scroll_x = max(0, min(self.scroll_x, max_scroll))

    def _delete_selection(self):
        start = min(self.selection_start, self.cursor_pos)
        end = max(self.selection_start, self.cursor_pos)
        self.text = self.text[:start] + self.text[end:]
        self.cursor_pos = start
        self.selection_start = start

    def _insert_text(self, string):
        if self.selection_start != self.cursor_pos:
            self._delete_selection()
        if self.max_length and len(self.text) + len(string) > self.max_length:
            string = string[:self.max_length - len(self.text)]
        self.text = self.text[:self.cursor_pos] + string + self.text[self.cursor_pos:]
        self.cursor_pos += len(string)
        self.selection_start = self.cursor_pos

    def _copy(self):
        if self.selection_start != self.cursor_pos:
            start = min(self.selection_start, self.cursor_pos)
            end = max(self.selection_start, self.cursor_pos)
            try:
                scrap.init()
                scrap.put(SCRAP_TEXT, self.text[start:end].encode('utf-8'))
            except:
                pass

    def _cut(self):
        self._copy()
        self._delete_selection()

    def _paste(self):
        try:
            scrap.init()
            t = scrap.get(SCRAP_TEXT).decode('utf-8').strip('\x00')
            self._insert_text(t)
        except:
            pass

    def update(self):
        if not self.visible:
            self.is_hovered = False
            return
            
        mouse_pos = mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered:
            mouse.set_cursor(CURSORS["ibeam"])
        elif was_hovered and not self.is_hovered:
            mouse.set_cursor(CURSORS["arrow"])
            
        if self.is_focused:
            if time.get_ticks() - self.last_blink > 500:
                self.cursor_visible = not self.cursor_visible
                self.last_blink = time.get_ticks()
        else:
            self.cursor_visible = False

    def handle_event(self, event):
        if not self.visible: return
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered:
                    self.is_focused = True
                    key.set_repeat(300, 50)
                    self.cursor_pos = self._get_index_from_mouse(event.pos)
                    self.selection_start = self.cursor_pos
                    self.is_dragging = True
                    self.cursor_visible = True
                    self.last_blink = time.get_ticks()
                else:
                    self.is_focused = False
                    self.selection_start = self.cursor_pos
                    
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                
        elif event.type == MOUSEMOTION:
            if self.is_dragging:
                self.cursor_pos = self._get_index_from_mouse(event.pos)
                self.cursor_visible = True
                self.last_blink = time.get_ticks()
                self._adjust_scroll()
                
        elif event.type == KEYDOWN and self.is_focused:
            ctrl = key.get_mods() & KMOD_CTRL
            shift = key.get_mods() & KMOD_SHIFT
            
            if ctrl:
                if event.key == K_a:
                    self.selection_start = 0
                    self.cursor_pos = len(self.text)
                elif event.key == K_c:
                    self._copy()
                elif event.key == K_x:
                    self._cut()
                elif event.key == K_v:
                    self._paste()
            else:
                if event.key == K_LEFT:
                    if shift:
                        self.cursor_pos = max(0, self.cursor_pos - 1)
                    else:
                        if self.selection_start != self.cursor_pos:
                            self.cursor_pos = min(self.selection_start, self.cursor_pos)
                            self.selection_start = self.cursor_pos
                        else:
                            self.cursor_pos = max(0, self.cursor_pos - 1)
                            self.selection_start = self.cursor_pos
                elif event.key == K_RIGHT:
                    if shift:
                        self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                    else:
                        if self.selection_start != self.cursor_pos:
                            self.cursor_pos = max(self.selection_start, self.cursor_pos)
                            self.selection_start = self.cursor_pos
                        else:
                            self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                            self.selection_start = self.cursor_pos
                elif event.key == K_HOME:
                    self.cursor_pos = 0
                    if not shift: self.selection_start = 0
                elif event.key == K_END:
                    self.cursor_pos = len(self.text)
                    if not shift: self.selection_start = self.cursor_pos
                elif event.key == K_BACKSPACE:
                    if self.selection_start != self.cursor_pos:
                        self._delete_selection()
                    elif self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                        self.selection_start = self.cursor_pos
                elif event.key == K_DELETE:
                    if self.selection_start != self.cursor_pos:
                        self._delete_selection()
                    elif self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    pass
                else:
                    if event.unicode and ord(event.unicode) >= 32:
                        self._insert_text(event.unicode)
            
            self.last_blink = time.get_ticks()
            self.cursor_visible = True
            self._adjust_scroll()

    def draw(self, screen):
        if not self.visible: return
        self._render_shape()
        
        inner_rect = Rect(self.padding_x, 0, self.rect.width - 2 * self.padding_x, self.rect.height)
        inner_surf = Surface(inner_rect.size, SRCALPHA)
        
        disp_text = self._get_display_text()
        
        if not disp_text and not self.is_focused:
            p_surf = self.font.render(self.placeholder_text, True, self.placeholder_text_color)
            inner_surf.blit(p_surf, (-self.scroll_x, (self.rect.height - p_surf.get_height()) // 2))
        else:
            if self.selection_start != self.cursor_pos:
                start = min(self.selection_start, self.cursor_pos)
                end = max(self.selection_start, self.cursor_pos)
                x1 = self.font.size(disp_text[:start])[0] - self.scroll_x
                x2 = self.font.size(disp_text[:end])[0] - self.scroll_x
                draw.rect(inner_surf, self.selection_color, (x1, 0, x2 - x1, self.rect.height))
            
            t_surf = self.font.render(disp_text, True, self.text_color)
            inner_surf.blit(t_surf, (-self.scroll_x, (self.rect.height - t_surf.get_height()) // 2))
            
            if self.is_focused and self.cursor_visible:
                cx = self.font.size(disp_text[:self.cursor_pos])[0] - self.scroll_x
                draw.line(inner_surf, self.cursor_color, (cx, 4), (cx, self.rect.height - 4), 2)
                
        if self.is_focused:
            draw.rect(self.surface, self.focused_border_color, (0, 0, self.rect.width, self.rect.height), self.border_width, self.border_radius)
        elif self.border_width > 0:
            draw.rect(self.surface, self.border_color, (0, 0, self.rect.width, self.rect.height), self.border_width, self.border_radius)
            
        self.surface.blit(inner_surf, inner_rect.topleft)
        screen.blit(self.surface, self.rect.topleft)

class ScrollingFrame(UIElement):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.elements = []
        self.scroll_y = 0
        self.content_height = height
        
    def add_element(self, element):
        element.base_y = element.y
        element.base_x = element.x
        self.elements.append(element)
        self.content_height = max(self.content_height, element.base_y + element.rect.height + 20)
        
    def update(self):
        for el in self.elements:
            el.y = self.rect.y + el.base_y - self.scroll_y
            el.x = self.rect.x + el.base_x
            el.update()
            
    def handle_event(self, event):
        if not self.visible: return
        if event.type == MOUSEWHEEL:
            if self.rect.collidepoint(mouse.get_pos()):
                self.scroll_y -= event.y * 30
                max_scroll = max(0, self.content_height - self.rect.height)
                self.scroll_y = max(0, min(self.scroll_y, max_scroll))
        for el in self.elements:
            if self.rect.collidepoint(mouse.get_pos()) or getattr(event, 'type', None) not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                el.handle_event(event)
                
    def draw(self, screen):
        if not self.visible: return
        self._render_shape()
        clip_rect = self.rect.copy()
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)
        screen.blit(self.surface, self.rect.topleft)
        for el in self.elements:
            if el.y + el.rect.height > self.rect.y and el.y < self.rect.y + self.rect.height:
                el.draw(screen)
        screen.set_clip(old_clip)