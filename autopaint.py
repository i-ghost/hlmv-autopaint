# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import tkMessageBox as tkBox
import tkColorChooser as tkColor
from ConfigParser import ConfigParser

class RootFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.init_config()
        self.init_left_frame()
        self.init_right_frame()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_delete)

    def on_delete(self):
        """Update configuration file on exit"""
        config_save = ConfigParser()
        try:
            config_save.add_section("User")
            config_save.add_section("Paints")
        except ConfigParser.DuplicateSectionError:
            pass
        for paint in sorted(self.paints):
            config_save.set("Paints", paint, self.paints[paint])
        config_save.set("User", "username", self.config["username"])
        with open("config.cfg", "wt") as config_file:
            config_save.write(config_file)
        self.parent.destroy()
        
    def reset_config(self):
        pass
        # reset config stuff goes here
        
    def init_config(self):
        self.paints = {}
        self.config = {}
        config = ConfigParser()
        config_file = os.path.join(os.getcwd(), "config.cfg")
        try:
            config.read(config_file)
            # Paints
            for paint in config.items("Paints"):
                self.paints[paint[0]] = paint[1]
            # User/Pass
            for i in config.items("User"):
                self.config[i[0]] = i[1]
        except Exception, e:
            import sys, traceback
            traceback.print_exc()
            tkBox.showerror("Error", e)
            sys.exit(1)
            
    def init_ui(self):
        self.parent.title("hlmv automator")
        self.parent.wm_iconbitmap("hlmv.ico")
        self.parent.resizable(False, False)
        self.pack(fill=tk.BOTH, expand=1)
        
        # geometry
        width = 580
        height = 350
        # center window
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - width)/2
        y = (screen_height - height)/2
        
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    def init_left_frame(self):
        left_frame = tk.Frame(self)#, background="green")
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, pady=10, padx=10)
        
        def on_cb_click():
            if self.int_upload_var.get() == 1:
                in_wiki_user.config(state=tk.NORMAL)
                in_wiki_pass.config(state=tk.NORMAL)
            else:
                in_wiki_user.config(state=tk.DISABLED)
                in_wiki_pass.config(state=tk.DISABLED)
        
        
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
        in_wiki_user = tk.Entry(left_frame)
        in_wiki_user.insert(0, self.config["username"])
        in_wiki_user.config(state=tk.DISABLED)
        in_wiki_user.grid(row=5, column=1)
        
        in_wiki_pass = tk.Entry(left_frame, show="*")
        in_wiki_pass.config(state=tk.DISABLED)
        in_wiki_pass.grid(row=6, column=1)
        

    def init_right_frame(self):
        right_frame = tk.Frame(self)#, background="purple")
        right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)
        self.str_paints_var = tk.StringVar()
        self.str_paintname_var = tk.StringVar()   
        
        def _assert():
            assert self.lst_paints.size() == len(self.paints)

        def on_paint_select(val):
            """Update tk string variables on listbox select"""
            w = val.widget
            v = w.get(w.curselection()[0])
            self.str_paints_var.set(v.split()[0].strip())
            self.str_paintname_var.set(" ".join(v.split()[1:]))

        def on_paint_edit():
            """Open a color picker and return hex value"""
            color = "#%s" % (self.str_paints_var.get())
            if color == "#":
                color = "white"
            (rgb, hex) = tkColor.askcolor(color)
            # Returns None on cancel
            if hex is not None:
                self.str_paints_var.set(hex.lstrip("#"))
            print self.paints
            _assert()
            
        def on_paint_add():
            """Add the paint to the listbox and update paint dictionary"""
            if self.str_paintname_var.get() in self.paints or self.str_paintname_var.get() == "" or self.str_paints_var.get() == "":
                # Don't add if already exists or inputs are empty
                return
            paintname = " ".join(self.str_paintname_var.get().split())
            self.paints[paintname] = self.str_paints_var.get()
            self.lst_paints.insert(tk.END, "%s %s" % (self.str_paints_var.get(), paintname))
            self.str_paintname_var.set("")
            print self.paints
            _assert()
            
        def on_paint_delete():
            """Remove paint from the listbox and update paint dictionary"""
            paintname = " ".join(self.lst_paints.get(tk.ANCHOR).split(" ", 1)[1:])
            print("Selection: %s" % (paintname))
            try:
                del self.paints[paintname]
                self.lst_paints.delete(tk.ANCHOR)
            except KeyError:
                pass
                # Log this in the future

        # Paint label
        lbl_paints = tk.Label(right_frame, text="Paints")
        lbl_paints.grid(padx=10, sticky=tk.W)
                
        # Scrollbar
        scrl_paints = tk.Scrollbar(right_frame, relief=tk.SUNKEN)
        scrl_paints.grid(column=2, sticky=tk.N+tk.S)
        
        # Paint list        
        self.lst_paints = tk.Listbox(right_frame, selectmode=tk.SINGLE, activestyle=tk.DOTBOX, width=45, yscrollcommand=scrl_paints.set)
        self.lst_paints.grid(row=1, padx=5, pady=5, columnspan=2)
        
        scrl_paints["command"] = self.lst_paints.yview
        
        self.lst_paints.bind("<<ListboxSelect>>", on_paint_select)
        
        for paint in sorted(self.paints):
            self.lst_paints.insert(tk.END, "%s %s" % (self.paints[paint], paint))
        
        # Paint editing interface
        # Paint name
        in_paintname_edit = tk.Entry(right_frame, textvariable=self.str_paintname_var)
        in_paintname_edit.grid(row=2, columnspan=2, sticky=tk.W+tk.E)
        
        # Color picker
        btn_paint_edit = tk.Button(right_frame, text="Pick color", command=on_paint_edit)
        btn_paint_edit.grid(row=3, column=0, sticky=tk.W+tk.E, columnspan=2)
        
        # Add color
        btn_paint_add = tk.Button(right_frame, text="Add paint", command=on_paint_add)
        btn_paint_add.grid(row=4, column=0, sticky=tk.W+tk.E)
        
        # Delete color
        btn_paint_save = tk.Button(right_frame, text="Delete paint", command=on_paint_delete)
        btn_paint_save.grid(row=4, column=1, sticky=tk.W+tk.E)
        
        # Color preview
        
        
        
def main():
    root = tk.Tk()
    app = RootFrame(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()