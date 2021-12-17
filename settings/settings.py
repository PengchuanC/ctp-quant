import platform
import sys
from pathlib import Path


DEBUG = False


cwd = Path(__file__).resolve(strict=True).parent.parent
sys.path.insert(0, rf'{cwd}')
lib = cwd / 'ctp'
arch = platform.system()

lib /= 'debug' if DEBUG else 'release'
lib = lib / 'win64' if arch == 'Windows' else 'linux'
sys.path.append(rf'{lib}')

USERINFO = cwd / 'userinfo'
