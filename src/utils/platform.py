import sys
try:
    import distro
except:
    pass

def get_platform():
    p = sys.platform
    if p == "linux":
        return f"GNU/Linux {distro.name()}"
    elif p == "win32":
        return "Windows"
    elif p == "darwin":
        return "MacOS"