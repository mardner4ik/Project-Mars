import pygame
import os
from pathlib import Path

class ImageManager:
    
    def __init__(self):
        self.images_cache = {}
        self.assets_dir = Path(__file__).parent.parent / 'assets/images'
    
    def load_image(self, filename, width=None, height=None, cache=True):
        
        cache_key = f"{filename}_{width}_{height}"
        if cache_key in self.images_cache:
            return self.images_cache[cache_key]
        
        image_path = self.assets_dir / filename
        
        if not image_path.exists():
            print(f"Зображення не знайдено: {image_path}")
            return None
        
        try:
            image = pygame.image.load(str(image_path))
            
            if width and height:
                image = pygame.transform.scale(image, (int(width), int(height)))
            
            if cache:
                self.images_cache[cache_key] = image
            
            return image
        except Exception as e:
            print(f"Помилка при завантаженні зображення {filename}: {e}")
            return None
    
    def create_gradient_surface(self, width, height, color1, color2, direction='vertical'):
        
        surface = pygame.Surface((width, height))
        
        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        else:
            for x in range(width):
                ratio = x / width
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        
        return surface

image_manager = ImageManager()
