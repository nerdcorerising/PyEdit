import tkinter as tk

def createFileMenu(master):
    filemenu = tk.Menu(master, tearoff=0)
    filemenu.add_command(label="Open File", command=master.master.openFile)
    filemenu.add_command(label="Save", command=master.master.saveCurrent)
    filemenu.add_command(label="Save As...", command=master.master.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=master.master.quit)
    return filemenu
    
def createEditMenu(master):
    editmenu = tk.Menu(master, tearoff=0)
    editmenu.add_command(label="Undo",command=master.master.undo)
    editmenu.add_command(label="Redo",command=master.master.redo)
    editmenu.add_command(label="Word Count",command=master.master.updateWordCount)
    return editmenu
    
def createOptionsMenu(master,control,control2,fontlist):
    optionsmenu = tk.Menu(master, tearoff=0)
    optionsmenu.add_checkbutton(label="Word Wrap", command=master.master.wordWrap)
    
    #Add the fonts to the menu
    font = tk.Menu(master, tearoff=0)
    listtemp = []
    for f in fontlist:
        #Weed out the spammy ones. This still leaves a TON!
        if(not(f[0] == "@" or f.find("UPC") > -1 or f.find("Ming") > -1
            or f.find("Mathematica") > -1 or f.find("Microsoft") > -1)):
            listtemp.append(f)
            
    listtemp.sort()
    for f in listtemp:
        font.add_radiobutton(label=f,variable=control2,value=f,command=master.master.setFontType)
    optionsmenu.add_cascade(label="Font",menu=font)
    
    #Add the font sizes to the menu
    font = tk.Menu(master, tearoff=0)
    for i in range (6,50,2):
        s = str(i) + " pt."
        font.add_radiobutton(label=s,variable=control,value=i,command=master.master.setFontSize)
    optionsmenu.add_cascade(label="Font Size",menu=font)

    return optionsmenu
    
if __name__ == "__main__":
    print ("Menus is a library.")