# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import tkMessageBox
import tkColorChooser
import tkFileDialog
import ctypes
import struct
import windowswitcher
from ConfigParser import SafeConfigParser

def send_f5():
    """Sends an F5 to the active window"""
    ctypes.windll.user32.keybd_event(0x74, 0, 0, 0) # F5 down
    ctypes.windll.user32.keybd_event(0x74, 0, 0x0002, 0) # F5 up

def hex_to_rgb(i):
    """Takes a hex value and returns a string containing RGB values"""
    return " ".join(map(str,struct.unpack('BBB',i.decode('hex'))))    
    

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

        except Exception, e:
            # Stop here if we can't load the configuration for whatever reason
            import sys, traceback
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
        
        def on_cb_click():
            if self.int_upload_var.get():
                self.in_wiki_user.config(state=tk.NORMAL)
                self.in_wiki_pass.config(state=tk.NORMAL)
            else:
                self.in_wiki_user.config(state=tk.DISABLED)
                self.in_wiki_pass.config(state=tk.DISABLED)

        def on_red_file_select():
            file = tkFileDialog.askopenfilename(title="Specify RED vmt", filetypes=[("Valve material", "*.vmt")])
            if file:
                self.red_vmt = file
                print self.red_vmt

        def on_blu_file_select():
            file = tkFileDialog.askopenfilename(title="Specify BLU vmt", filetypes=[("Valve material", "*.vmt")])
            if file:
                self.blu_vmt = file
                print self.blu_vmt
                
        def on_start_automator():
            pass
            # switch to hlmv
            # for each paint in red listbox, replace $color2 \
            # in red vmt with rgb using hex_to_rgb()
            # repeat with blu vmt
            # call threaded blender
            # done
            # w = windowswitcher.WindowSwitcher()
            # w.activate(wildcard=r".*?.mdl")
            # send_f5()
            # model = w.get_last_window_name()

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