# -*- coding: utf-8 -*-

import Tkinter as tk

class RootFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.init_left_frame()
        self.init_right_frame()     
        
    def init_ui(self):
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
        left_frame = tk.Frame(self)#, background="green")
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, pady=10, padx=10)
        
        def on_cb_click():
            if self.upload_var.get() == 1:
                in_wiki_user.config(state=tk.NORMAL)
                in_wiki_pass.config(state=tk.NORMAL)
            else:
                in_wiki_user.config(state=tk.DISABLED)
                in_wiki_pass.config(state=tk.DISABLED)
        
        # Checkbox
        self.upload_var = tk.IntVar()
        cb_upload_wiki = tk.Checkbutton(left_frame, text="Upload to Wiki", variable=self.upload_var, command=on_cb_click)
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
        self.lst_paints_var = tk.StringVar()
        self.lst_paintname_var = tk.StringVar()   
        
        def on_paint_select(val):
            w = val.widget
            v = w.get(w.curselection()[0])
            self.lst_paints_var.set(v.split()[0])
            self.lst_paintname_var.set(" ".join(v.split()[1:]))
        
        # Paint label
        lbl_paints = tk.Label(right_frame, text="Paints")
        lbl_paints.grid(padx=10)
                
        # Paint list        
        lst_paints = tk.Listbox(right_frame, selectmode=tk.SINGLE, activestyle=tk.DOTBOX, width=45)
        lst_paints.grid(row=1, padx=5, pady=5)
        
        # Scrollbar
        scrl_paints = tk.Scrollbar(right_frame, command=lst_paints.yview)
        scrl_paints.grid(row=1, column=1)
        lst_paints.yscrollcommand = scrl_paints.set
        
        lst_paints.bind("<<ListboxSelect>>", on_paint_select)
        
        paints = {"An Extraordinary Abundance of Tinge": "E6E6E6",
				"Color No. 216-190-216": "D8BED8",
				"Peculiarly Drab Tincture": "C5AF91",
				"Aged Moustache Grey": "7E7E7E",
				"A Distinctive Lack of Hue": "141414",
				"After Eight": "2D2D24",
				"Radigan Conagher Brown": "694D3A",
				"Ye Olde Rustic Color": "7C6C57",
				"Muskelmannbraun": "A57545",
				"Australium Gold": "E7B53B",
				"The Color of a Gentlemann's Business Pants": "F0E68C",
				"Dark Salmon Injustice": "E9967A",
				"Mann Co. Orange": "CF7336",
				"Pink as Hell": "FF69B4",
				"A Deep Commitment to Purple": "7D4071",
				"Noble Hatter's Violet": "51384A",
				"A Color Similar to Slate": "2F4F4F",
				"The Bitter Taste of Defeat and Lime": "32CD32",
				"Indubitably Green": "729E42",
			 	"A Mann's Mint": "BCDDB3",
				"Drably Olive": "808000",
				"Zephaniah's Greed": "424F3B",
				"Waterlogged Lab Coat (RED)": "A89A8C",
				"Balaclavas Are Forever (RED)": "3B1F23",
				"Team Spirit (RED)": "B8383B",
				"Operator's Overalls (RED)": "483838",
				"The Value of Teamwork (RED)": "803020",
				"An Air of Debonair (RED)": "654740",
				"Cream Spirit (RED)": "C36C2D",
				"Waterlogged Lab Coat (BLU)": "839FA3",
				"Balaclavas Are Forever (BLU)": "18233D",
				"Team Spirit (BLU)": "5885A2",
				"Operator's Overalls (BLU)": "384248",
				"The Value of Teamwork (BLU)": "256D8D",
				"An Air of Debonair (BLU)": "28394D",
				"Cream Spirit (BLU)": "B88035"
				}
        
        for paint in paints:
            lst_paints.insert(tk.END, "%s (%s)" % (paints[paint], paint))
            
        in_paint_edit = tk.Entry(right_frame, textvariable=self.lst_paints_var, width=50)
        in_paint_edit.grid(row=2)
        
        in_paintname_edit = tk.Entry(right_frame, textvariable=self.lst_paintname_var, width=50)
        in_paintname_edit.grid(row=3, pady=5)
        
        
class LogFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
def main():
    root = tk.Tk()
    app = RootFrame(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()