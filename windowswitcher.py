# -*- coding: utf-8 -*-
"""
Window Switching Module
Provides WindowSwitcher class to bring different windows to foreground
i-ghost
"""
import ctypes, os, re, sys

# No pywin32 as it does not expose AllowSetForegroundWindow() and this doesn't need much else from it anyway
_user32 = ctypes.windll.user32
# callback prototype
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

class WindowSwitcher(object):
    """A WindowSwitcher class allowing one to switch between windows using the activate method
    If wrapped using the with statement, the initial window is returned to the foreground on completion of the with block
    >>> from windowswitcher import WindowSwitcher
    >>> import subprocess, os, time
    >>> notepad = subprocess.Popen(os.path.join(os.environ["WINDIR"], "notepad.exe"))
    >>> with WindowSwitcher() as w:
    ...     time.sleep(2)
    ...     w.activate(window_name = "Untitled - Notepad")
    ...     print w.history.keys()
    [u'Untitled - Notepad']
    >>> notepad.kill()
    """
    def __enter__(self):
        # dirty dirty hack here as pywin32 does not expose AllowSetForegroundWindow()
        #self.fg_lock = win32con.SPI_GETFOREGROUNDLOCKTIMEOUT
        #win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE)
        return self

    def __init__(self):
        self._handle = None
        self.parent = _user32.GetForegroundWindow()
        self.history = {}
        self.last_window_text = None
        _user32.AllowSetForegroundWindow(os.getpid())
        
    def _add_to_history(self):
        window_text = self._get_window_text(self._handle)
        self.last_window_text = window_text
        if window_text not in self.history:
            self.history[window_text] = ctypes.cast(self._handle, ctypes.c_void_p).value
            
    def _get_window_text(self, handle):
        length = _user32.GetWindowTextLengthW(handle) + 1
        buff = ctypes.create_unicode_buffer(length)
        _user32.GetWindowTextW(handle, buff, length)
        return buff.value

    def _window_enum_callback(self, handle, wildcard):
        """Pass to EnumWindows() to check all the opened windows"""
        wildcard = ctypes.cast(wildcard, ctypes.c_wchar_p).value.encode("utf-8")
        if re.match(wildcard, self._get_window_text(handle)):
            self._handle = handle

    def _find_window(self, class_name, window_name):
        """Find a window by its class or window name"""
        self._handle = _user32.FindWindowW(ctypes.c_wchar_p(class_name), ctypes.c_wchar_p(window_name))

    def _find_window_wildcard(self, wildcard):
        """Find window by wildcard by enumerating over existing windows"""
        self._handle = None
        _user32.EnumWindows(EnumWindowsProc(self._window_enum_callback), ctypes.c_wchar_p(wildcard))

    def _set_foreground(self, force):
        """Brings a given window to the foreground"""
        if force:
            _user32.ShowWindow(self._handle, 9)
        _user32.SetForegroundWindow(self._handle)
        
    def activate(self, name = None, class_name = None, window_name = None, wildcard = None, force = False):
        """Activates a window
        If specifying a window by class/exact name, use class_name and window_name parameters
        If the window name is volatile, use the wildcard option, which accepts a regular expression
        Specify false if the target window is minimized
        Activated window names are stored, so previous entries can be activated using the name parameter
        """
        if name:
            try:
                self._handle = self.history[name]
            except KeyError:
                pass
        elif wildcard:
            self._find_window_wildcard(wildcard)
        elif class_name or window_name:
            self._find_window(class_name, window_name)
        if self._handle:
            self._set_foreground(force)
            self._add_to_history()
            
    def get_last_window_name(self):
        if self.last_window_text:
            return self.last_window_text
            
    def __exit__(self, type, value, traceback):
        """return foreground lock to initial state and return to initial window"""
        self._handle = self.parent
        self._set_foreground(False)
        # cleanup for dirty dirty hack
        #win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, self.WindowSwitcher.fg_lock, win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE)
        
    def __str__(self):
        return "WindowSwitcher class"
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()