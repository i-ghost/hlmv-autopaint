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
            assert len(self.paints) > 0
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
        width = 530
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
        
        # Checkbox
        self.int_upload_var = tk.IntVar()
        cb_upload_wiki = tk.Checkbutton(left_frame, text="Upload to Wiki", variable=self.int_upload_var, command=on_cb_click)
        cb_upload_wiki.grid(row=0, sticky=tk.W, pady=10, columnspan=2)
        
        # Text labels
        lbl_wiki_user = tk.Label(left_frame, text="Username:")
        lbl_wiki_user.grid(row=1, sticky=tk.W)
        
        lbl_wiki_pass = tk.Label(left_frame, text="Password:")
        lbl_wiki_pass.grid(row=2, sticky=tk.W, pady=5)
        
        # Text input
        in_wiki_user = tk.Entry(left_frame)
        in_wiki_user.insert(0, "Username")
        in_wiki_user.config(state=tk.DISABLED)
        in_wiki_user.grid(row=1, column=1)
        
        in_wiki_pass = tk.Entry(left_frame, show="*")
        in_wiki_pass.config(state=tk.DISABLED)
        in_wiki_pass.grid(row=2, column=1)

    def init_right_frame(self):
        right_frame = tk.Frame(self)#, background="purple")
        right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)
        self.str_paints_var = tk.StringVar()
        self.str_paintname_var = tk.StringVar()   
        
        def on_paint_select(val):
            w = val.widget
            v = w.get(w.curselection()[0])
            self.str_paints_var.set(v.split(":")[0].strip())
            self.str_paintname_var.set(" ".join(v.split(":")[1:]))
            
        def on_paint_edit():
            color = "#%s" % (self.str_paints_var.get())
            (rgb, hex) = tkColor.askcolor(color)
            
        def on_paint_save():
            pass
            # Update config file here
        
        # Paint label
        lbl_paints = tk.Label(right_frame, text="Paints")
        lbl_paints.grid(padx=10)
                
        # Scrollbar
        scrl_paints = tk.Scrollbar(right_frame, relief=tk.SUNKEN)
        scrl_paints.grid(column=2, sticky=tk.N+tk.S)
        
        # Paint list        
        lst_paints = tk.Listbox(right_frame, selectmode=tk.SINGLE, activestyle=tk.DOTBOX, width=45, yscrollcommand=scrl_paints.set)
        lst_paints.grid(row=1, padx=5, pady=5, columnspan=2)
        
        scrl_paints["command"] = lst_paints.yview
        
        lst_paints.bind("<<ListboxSelect>>", on_paint_select)
        
        for paint in self.paints:
            lst_paints.insert(tk.END, "%s : %s" % (self.paints[paint], paint))
        
        # Paint editing interface
        # Paint name
        in_paintname_edit = tk.Entry(right_frame, textvariable=self.str_paintname_var)
        in_paintname_edit.grid(row=2, columnspan=2, sticky=tk.W+tk.E)
        
        # Color picker
        btn_paint_edit = tk.Button(right_frame, text="Edit color", command=on_paint_edit)
        btn_paint_edit.grid(row=3, column=0, sticky=tk.W+tk.E)
        
        # Commit changes
        btn_paint_save = tk.Button(right_frame, text="Save changes", command=on_paint_save)
        btn_paint_save.grid(row=3, column=1, sticky=tk.W+tk.E)
        
        
def main():
    root = tk.Tk()
    app = RootFrame(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()