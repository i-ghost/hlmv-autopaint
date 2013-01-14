import os
import subprocess
import ImageGrab

_nirCmd = os.path.join(os.path.abspath(os.path.dirname(__file__)), "nircmdc.exe")

_cmdFlags = subprocess.STARTUPINFO()
_cmdFlags.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def screenshot():
    """User nircmd to save a screenshot of the active window to the clipboard and return it as a PIL image object"""
    subprocess.Popen("%s savescreenshot *clipboard*" % (_nirCmd), startupinfo=_cmdFlags).communicate()
    return ImageGrab.grabclipboard()