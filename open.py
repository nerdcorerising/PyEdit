
from tkinter import *
from tkinter.messagebox import *
from tkinter.colorchooser import askcolor              
from tkinter.filedialog   import askopenfilename      

def callback():
    askopenfilename() 
    
    
errmsg = 'Error!'
Button(text='Quit', command=callback).pack(fill=X)
Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
mainloop()


     