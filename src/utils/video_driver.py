import os
import sys

from OpenGL.GL import glGetString, GL_VERSION

def pre_init_driver():
    if sys.platform == "linux":
        session = os.environ.get('XDG_SESSION_TYPE', '').lower()
        if session == "wayland":
            os.environ["SDL_VIDEODRIVER"] = "wayland,x11"
        else:
            os.environ["SDL_VIDEODRIVER"] = "x11"

def get_video_driver(display):
    try:
        version = glGetString(GL_VERSION).decode("utf-8")
    except Exception as err:
        print(f"Error: {err}")
        version = "Native Drivers"
    
    return f"{display.get_driver()} | {version}"