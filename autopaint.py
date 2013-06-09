# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import tkMessageBox
import tkColorChooser
import tkFileDialog
import ctypes
import shutil
import struct
import re
import time
import sys
import windowswitcher
import _winreg
import Image
import ImageGrab
import ImageChops
from nircmd import screenshot
from ConfigParser import SafeConfigParser

screenshot = screenshot.screenshot

def get_brightness(p):
    """CCIR601 RGB -> Luma conversion"""
    return (299.0 * p[0] + 587.0 * p[1] + 114.0 * p[2]) / 1000.0

def trim(im):
    """Removes all whitespace surrounding image"""
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def to_alpha_black_white(black_img, white_img):
    """Takes images with white/black background and returns a transparent image"""
    size = black_img.size
    black_img = black_img.convert('RGBA')
    loadedBlack = black_img.load()
    loadedWhite = white_img.load()
    for x in range(size[0]):
        for y in range(size[1]):
            blackPixel = loadedBlack[x, y]
            whitePixel = loadedWhite[x, y]
            loadedBlack[x, y] = (
                (blackPixel[0] + whitePixel[0]) / 2,
                (blackPixel[1] + whitePixel[1]) / 2,
                (blackPixel[2] + whitePixel[2]) / 2,
                int(255.0 - 255.0 * (get_brightness(whitePixel) - get_brightness(blackPixel)))
            )
    return black_img

def send_f5():
    """Sends an F5 to the active window"""
    ctypes.windll.user32.keybd_event(0x74, 0, 0, 0) # F5 down
    ctypes.windll.user32.keybd_event(0x74, 0, 0x0002, 0) # F5 up
    
def _send_printscr():
    """Sends an ALT+PRINTSCR to the active window"""
    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0) # ALT down
    ctypes.windll.user32.keybd_event(0x2C, 0, 0, 0) # PRINTSCR down
    ctypes.windll.user32.keybd_event(0x2C, 0, 0x0002, 0) # PRINTSCR up
    ctypes.windll.user32.keybd_event(0x12, 0, 0x0002, 0) # ALT up

def hex_to_rgb(i):
    """Takes a hex value and returns a string containing RGB values"""
    return " ".join(map(str,struct.unpack('BBB',i.decode('hex'))))
    
def read_regkey(k, v):
	"""Convenience function to read registry data"""
	return _winreg.QueryValueEx(k, v)[0]

# def screenshot():
    # """Returns a PIL object of a screenshot of the current active foreground window"""
    # _send_printscr()
    # img = ImageGrab.grabclipboard()
    # return img


class PaintSelector(object):
    """An iterable listbox with scrollbar and three buttons to control it"""
    def __init__(self, frame, title="Paints", columnn_offset=0, row_offset=0):
        self.frame = frame
        self.title = title
        self.column_offset = columnn_offset
        self.row_offset = row_offset
        self.str_paint_var = tk.StringVar()
        self.str_paintname_var = tk.StringVar()
        self.init_widgets()
        
    def __iter__(self):
        for i in self.listbox.get(0, tk.END):
            yield i

    def init_widgets(self):
        # Paint label
        label = tk.Label(self.frame, text=self.title)
        label.grid(padx=10, sticky=tk.W)
                
        # Scrollbar
        scrollbar = tk.Scrollbar(self.frame, relief=tk.SUNKEN)
        scrollbar.grid(column=self.column_offset+2, sticky=tk.N+tk.S)
        
        # Paint list        
        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, activestyle=tk.DOTBOX, width=45, yscrollcommand=scrollbar.set)
        self.listbox.grid(row=self.row_offset+1, padx=5, pady=5, columnspan=2)
        
        scrollbar["command"] = self.listbox.yview
        
        self.listbox.bind("<<ListboxSelect>>", self.on_paint_select)
        
        
        # Paint editing interface
        # Paint name
        paint_entry = tk.Entry(self.frame, textvariable=self.str_paintname_var)
        paint_entry.grid(row=self.row_offset+2, columnspan=2, sticky=tk.W+tk.E)
        
        # Color picker
        paint_edit = tk.Button(self.frame, text="Pick color", command=self.on_paint_edit)
        paint_edit.grid(row=self.row_offset+3, column=self.column_offset+0, sticky=tk.W+tk.E, columnspan=2)
        
        # Add color
        paint_add = tk.Button(self.frame, text="Add paint", command=self.on_paint_add)
        paint_add.grid(row=self.row_offset+4, column=self.column_offset+0, sticky=tk.W+tk.E)
        
        # Delete color
        paint_save = tk.Button(self.frame, text="Delete paint", command=self.on_paint_delete)
        paint_save.grid(row=self.row_offset+4, column=self.column_offset+1, sticky=tk.W+tk.E)


    def insert(self, i):
        self.listbox.insert(tk.END, i)

    def on_paint_select(self, val):
        """Update tk string variables on listbox select"""
        w = val.widget
        v = w.get(w.curselection()[0])
        self.str_paint_var.set(v.split()[0].strip())
        self.str_paintname_var.set(" ".join(v.split()[1:]))

    def on_paint_edit(self):
        """Open a color picker and return hex value"""
        color = "#%s" % (self.str_paint_var.get())
        if color == "#":
            color = "white"
        (rgb, hex) = tkColorChooser.askcolor(color)
        # Returns None on cancel
        if hex is not None:
            self.str_paint_var.set(hex.lstrip("#"))
        
    def on_paint_add(self):
        """Add the paint to the listbox"""
        if "%s %s" % (self.str_paint_var.get(), self.str_paintname_var.get()) in self.listbox.get(0, tk.END) \
        or self.str_paintname_var.get() == "" or self.str_paint_var.get() == "":
            # Don't add if already exists or inputs are empty
            return
        paintname = " ".join(self.str_paintname_var.get().split())
        self.listbox.insert(tk.END, "%s %s" % (self.str_paint_var.get(), paintname))
        self.str_paintname_var.set("")
        
    def on_paint_delete(self):
        """Remove paint from the listbox"""
        paintname = " ".join(self.listbox.get(tk.ANCHOR).split(" ", 1)[1:])
        try:
            self.listbox.delete(tk.ANCHOR)
        except Exception:
            pass
            # Log this in the future

class RootFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.init_left_frame()
        self.init_middle_frame()
        self.init_right_frame()
        self.init_config()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_delete)

    def on_delete(self):
        """Update configuration file on exit"""
        config_save = SafeConfigParser()
        config_save.optionxform = str
        try:
            config_save.add_section("User")
            config_save.add_section("RED paints")
            config_save.add_section("BLU paints")
        except ConfigParser.DuplicateSectionError:
            pass
        # BLU paints
        for paint in sorted(self.blu_paintselector):
            # paint.split()[slice] is not passed directly to set() method as it raises a TypeError. bug?
            paint, paintname = paint.split()[0], " ".join(paint.split()[1:])
            config_save.set("BLU paints", paintname, paint)
        # RED paints
        for paint in sorted(self.red_paintselector):
            paint, paintname = paint.split()[0], " ".join(paint.split()[1:])
            config_save.set("RED paints", paintname, paint)
        config_save.set("User", "Username", self.in_wiki_user.get())
        config_save.set("User", "Upload", str(bool(self.int_upload_var.get())))
        with open("config.cfg", "wt") as config_file:
            config_save.write(config_file)
        self.parent.destroy()
        
    def reset_config(self):
        pass
        # reset config stuff goes here
        
    def init_config(self):
        self.config = {}
        config = SafeConfigParser()
        # Preserve case
        config.optionxform = str
        config_file = os.path.join(os.getcwd(), "config.cfg")
        try:
            config.read(config_file)
            # RED paints
            for paint in config.items("RED paints"):
                self.red_paintselector.insert(" ".join(reversed(paint)))
            # BLU paints
            for paint in config.items("BLU paints"):
                self.blu_paintselector.insert(" ".join(reversed(paint)))
            # User/Pass/Path
            for i in config.items("User"):
                self.config[i[0]] = i[1]
                
            self.config["Upload"] = config.getboolean("User", "Upload")
            self.in_wiki_user.insert(0, self.config["Username"])
            
            if self.config["Upload"]:
                self.int_upload_var.set(int(bool(self.config["Upload"])))
            else:
                self.in_wiki_user.config(state=tk.DISABLED)
                self.in_wiki_pass.config(state=tk.DISABLED)

            # Construct a path to the SteamPipe TF2 directory
            # Steam directory from registry
            steam_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam", 0, _winreg.KEY_ALL_ACCESS)
            steam_dir = read_regkey(steam_key, "SteamPath")
            _winreg.CloseKey(steam_key)
            tf2_dir = os.path.join(steam_dir, "steamapps", "common", "Team Fortress 2", "tf")
            hlmv_dir = os.path.join(tf2_dir, "custom", "hlmv autopaint", "materials", "hlmv")
            if not os.path.exists(hlmv_dir):
                os.makedirs(hlmv_dir)
            self.config["hlmv"] = hlmv_dir
            self.config["materials"] = os.path.join(hlmv_dir, os.pardir, "models", "player", "items")
            if not os.path.exists(self.config["materials"]):
                os.makedirs(self.config["materials"])
            # Remove fire overlay
            tiledfire_dir = os.path.join(self.config["hlmv"], os.pardir, "effects", "tiledfire")
            if not os.path.exists(tiledfire_dir):
                os.makedirs(tiledfire_dir)
            # Contrary to standard behaviour, creating a VMT with the same name does NOT override the VTF here.
            shutil.copy("resources/fireLayeredSlowTiled512.vtf", tiledfire_dir)

        except Exception, e:
            # Stop here if we can't load the configuration for whatever reason
            import traceback
            traceback.print_exc()
            tkMessageBox.showerror("Error", e)
            sys.exit(1)
            
    def init_ui(self):
        """Create the root geometry"""
        self.parent.title("hlmv automator")
        self.parent.wm_iconbitmap("hlmv.ico")
        self.parent.resizable(False, False)
        self.pack(fill=tk.BOTH, expand=1)
        
        # geometry
        width = 900
        height = 350
        # center window
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - width)/2
        y = (screen_height - height)/2
        
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    def init_left_frame(self):
        """Create the left frame"""
        left_frame = tk.Frame(self)#, background="green")
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, pady=10, padx=10)
        self.red_vmt = None
        self.blu_vmt = None
        
        def on_cb_click():
            self.in_wiki_user.config(state=tk.NORMAL) if self.int_upload_var.get() else self.in_wiki_user.config(state=tk.DISABLED)
            self.in_wiki_pass.config(state=tk.NORMAL) if self.int_upload_var.get() else self.in_wiki_pass.config(state=tk.DISABLED)

        def on_red_file_select():
            file = tkFileDialog.askopenfilename(title="Specify RED vmt", filetypes=[("Valve material", "*.vmt")], initialdir=self.config["materials"])
            if file:
                self.red_vmt = file

        def on_blu_file_select():
            file = tkFileDialog.askopenfilename(title="Specify BLU vmt", filetypes=[("Valve material", "*.vmt")], initialdir=self.config["materials"])
            if file:
                self.blu_vmt = file
                
        def write_vmt(f, color=None):
            """Replace $color2 {# # #} inside vmt file with value of color, or use $colortint_base"""
            with open(f, "rb") as vmt_file:
                vmt = vmt_file.read()
            color2_pattern = r'"?\$color2"?\s+"?\{(.[^\}]+)\}"?'
            color2_regex = re.compile(color2_pattern, re.IGNORECASE)
            color2_match = color2_regex.search(vmt)
            #
            base_pattern = r'"?\$colortint_base"?\s+"?\{(.[^\}]+)\}"?'
            base_regex = re.compile(base_pattern, re.IGNORECASE)
            base_match = base_regex.search(vmt)
            if base_match and not color2_match:
                # Create a $color2 if it doesn't exist
                vmt = re.sub(base_pattern, '"$colortint_base" "{%s}"\n\t"$color2" "{%s}"' % (
                            base_match.group(1),
                            color or base_match.group(1)),
                        vmt)
            elif color2_match:
                vmt = re.sub(color2_pattern, '"$color2" "{%s}"' % (color or base_match.group(1)), vmt)
            with open(f, "wb") as vmt_file:
                vmt_file.write(vmt)

        def alter_bg(color="255 255 255"):
            """Modify hlmv's background color, default to white"""
            bg_vmt = os.path.join(self.config["hlmv"], "background.vmt")
            vmt_base = '''"UnlitGeneric"\n{\n\t"$color" "{%s}"\n}'''
            with open(bg_vmt, "w+b") as vmt_file:
                vmt_file.write(vmt_base % (color))
                
        def _take_image(vmt, interval=2, paint=None, black=False):
            crop_boundaries = (1, 41, 1278, 743)
            if black:
                alter_bg(color="0 0 0")
                send_f5()
                time.sleep(interval)
                return screenshot().crop(crop_boundaries)
            if paint:
                write_vmt(vmt, color=hex_to_rgb(paint))
                alter_bg()
                send_f5()
                time.sleep(interval)
            else:
                write_vmt(vmt, color=None)
                alter_bg()
                send_f5()
                time.sleep(interval)
            return screenshot().crop(crop_boundaries)
                    

        def take_images(vmt, paints):
            """Take painted item images"""
            white, black = {}, {}
            for paint in paints:
                white[paint] = _take_image(vmt, paint=paint)
                black[paint] = _take_image(vmt, black=True)
            # Take stock item image
            white["UNPAINTED"] = _take_image(vmt, paint=None)
            black["UNPAINTED"] = _take_image(vmt, black=True)
            return white, black

        def on_start_automator():
            if self.red_vmt:
                # red_paints = [i.split()[0] for i in sorted(self.red_paintselector)]
                # blu_paints = [i.split()[0] for i in sorted(self.blu_paintselector)]
                red_paints = ["141414", "2D2D24"]
                blu_paints = ["18233D", "256D8D"]
                if not os.path.exists("png"):
                    os.mkdir("png")
                with windowswitcher.WindowSwitcher() as w:
                    w.activate(wildcard=r".*?.mdl", max=True, force=True)
                    if w.get_last_window_name():
                        paints_white, paints_black = take_images(self.red_vmt, red_paints)
                        if self.blu_vmt:
                            # Final filenames will be different if blu vmt exists
                            paints_white["RED"] = paints_white["UNPAINTED"]
                            paints_black["RED"] = paints_black["UNPAINTED"]
                            del(paints_white["UNPAINTED"], paints_black["UNPAINTED"])
                            # Replace red vmt with blu
                            os.rename(self.red_vmt, "%s~" % (self.red_vmt))
                            os.rename(self.blu_vmt, self.red_vmt)
                            blu_paints_white, blu_paints_black = take_images(self.red_vmt, blu_paints)
                            paints_white.update(blu_paints_white)
                            paints_black.update(blu_paints_black)
                            paints_white["BLU"] = paints_white["UNPAINTED"]
                            paints_black["BLU"] = paints_black["UNPAINTED"]
                            del(paints_white["UNPAINTED"], paints_black["UNPAINTED"])
                            del(blu_paints_white, blu_paints_black)
                            # Revert rename
                            os.rename(self.red_vmt, self.blu_vmt)
                            os.rename("%s~" % (self.red_vmt), self.red_vmt)
                for paint in paints_black:
                    final_image = trim(to_alpha_black_white(paints_black[paint], paints_white[paint]))
                    # BUG: Needs to run twice here to have an effect, but only once if trim() is used outside of program
                    final_image = trim(final_image)
                    if len(in_style.get()) > 0:
                        if paint in ["RED", "BLU"]:
                            final_image.save("png//%s_%s_%s.png" % (paint, in_item.get(), in_style.get()), "PNG")
                        else:
                            final_image.save("png//%s_%s_%s.png" % (in_item.get(), paint, in_style.get()), "PNG")
                    else:
                        if paint in ["RED", "BLU"]:
                            final_image.save("png//%s_%s.png" % (paint, in_item.get()), "PNG")
                        else:
                            final_image.save("png//%s_%s.png" % (in_item.get(), paint), "PNG")

        # Text labels
        lbl_settings = tk.Label(left_frame, text="Settings")
        lbl_settings.grid(sticky=tk.W, padx=10)
        
        lbl_item = tk.Label(left_frame, text="Item name:")
        lbl_item.grid(row=1, sticky=tk.W)
        
        lbl_style = tk.Label(left_frame, text="Style:")
        lbl_style.grid(row=2, sticky=tk.W)
        
        # Checkbox
        self.int_upload_var = tk.IntVar()
        cb_upload_wiki = tk.Checkbutton(left_frame, text="Upload to Wiki", variable=self.int_upload_var, command=on_cb_click)
        cb_upload_wiki.grid(row=4, sticky=tk.W, pady=10)
        
        # Wiki labels
        lbl_wiki_user = tk.Label(left_frame, text="Username:")
        lbl_wiki_user.grid(row=5, sticky=tk.W)
        
        lbl_wiki_pass = tk.Label(left_frame, text="Password:")
        lbl_wiki_pass.grid(row=6, sticky=tk.W, pady=5)
        
        # Text input
        
        # Settings
        in_item = tk.Entry(left_frame)
        in_item.grid(row=1, column=1)
        
        in_style = tk.Entry(left_frame)
        in_style.grid(row=2, column=1)
        
        # Wiki
        self.in_wiki_user = tk.Entry(left_frame)
        self.in_wiki_user.grid(row=5, column=1)
        
        self.in_wiki_pass = tk.Entry(left_frame, show="*")
        self.in_wiki_pass.grid(row=6, column=1)
        
        # RED file select button
        btn_file_select = tk.Button(left_frame, text="Select RED VMT", command=on_red_file_select)
        btn_file_select.grid(row=7, pady=5)

        # RED file select button
        btn_file_select = tk.Button(left_frame, text="Select BLU VMT", command=on_blu_file_select)
        btn_file_select.grid(row=7, column=1)
        
        # Start button
        btn_start = tk.Button(left_frame, text="Start", command=on_start_automator)
        btn_start.grid(row=8, rowspan=2, columnspan=2, sticky=tk.W+tk.E)
        

    def init_middle_frame(self):
        """Create the middle frame"""
        middle_frame = tk.Frame(self)#, background="purple")
        middle_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)
        
        self.red_paintselector = PaintSelector(middle_frame, title="RED paints")

    def init_right_frame(self):
        """Create the right frame"""
        right_frame = tk.Frame(self)
        right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)
        
        self.blu_paintselector = PaintSelector(right_frame, title="BLU paints")
        
        
def main():
    root = tk.Tk()
    app = RootFrame(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()