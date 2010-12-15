import tkinter

class Application(tkinter.Frame):              
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)   
        self.grid()         
        self.textboxrow = 0
        self.textboxcol = 0
        self.scrollcol = 1           
        self.createWidgets()

    def createWidgets(self):
        self.text = tkinter.Text(master=self)
        self.scroll = tkinter.Scrollbar(master=self)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.text.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        
        self.scroll.grid(column=self.scrollcol,row=self.textboxrow,sticky="ns")
        self.text.grid(column=self.textboxcol,row=self.textboxrow)
        


app = Application()                    
app.master.title("PyEdit") 
app.mainloop()    