import webbrowser

from .polygon import *
from .array import *
from .numbers import *
from .strings import *
from .utils import *
from .convert import *


def github():
    webbrowser.open("https://github.com/pranavbaburaj")


def credits():
    return "Created by Pranav Baburaj"


def explorer(location=os.getcwd()):
    try:
        os.listdir(location)
        webbrowser.open(location)
        return None
    except:
        return None
