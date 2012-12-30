# -*- coding: utf-8 -*-

import Tkinter as tk

class RootFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.init_left_area()
        self.init_right_area()
        
    def init_ui(self):
        self.parent.title("hlmv automator")
        self.parent.wm_iconbitmap("hlmv.ico")
        self.pack(fill=tk.BOTH, expand=1)
        
        # geometry
        width = 400
        height = 350
        # center window
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - width)/2
        y = (screen_height - height)/2
        
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    def init_left_area(self):
        left_frame = tk.Frame(self, background="green")
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=10, padx=5)
        
        cb_upload_wiki = tk.Checkbutton(left_frame, text="Upload to Wiki")
        cb_upload_wiki.pack(side=tk.TOP, expand=True)
        
        self.upload_var = tk.IntVar()
        
        txt_wiki_user = tk.Label(left_frame, text="Username")
        txt_wiki_user.pack(side=tk.LEFT, expand=False)
        
        txt_wiki_pass = tk.Label(left_frame, text="Password")
        txt_wiki_pass.pack(side=tk.LEFT, expand=False)
        
        in_wiki_user = tk.Entry(left_frame)
        in_wiki_user.pack(side=tk.LEFT, expand=True)
        
        in_wiki_pass = tk.Entry(left_frame)
        in_wiki_pass.pack(side=tk.LEFT, expand=True)
        
        def on_cb_click(self):
            if self.upload_var:
                in_wiki_pass.config(state=tk.DISABLED)
                in_wiki_user.config(state=tk.DISABLED)
        
    def init_right_area(self):
        right_frame= tk.Frame(self)
        right_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, pady=10, padx=5)
        
class LogFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
def main():
    root = tk.Tk()
    app = RootFrame(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()