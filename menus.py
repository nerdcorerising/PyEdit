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
    
    editmenu.add_separator()
    editmenu.add_command(labe="Copy",command=master.master.copy)
    editmenu.add_command(labe="Cut",command=master.master.cut)
    editmenu.add_command(labe="Paste",command=master.master.paste)
    
    editmenu.add_separator()
    editmenu.add_command(label="Word Count",command=master.master.updateWordCount)
    return editmenu
    
def createOptionsMenu(master,control,control2,fontlist):
    optionsmenu = tk.Menu(master, tearoff=0)
    optionsmenu.add_checkbutton(label="Word Wrap", command=master.master.wordWrap)
    optionsmenu.add_separator()
    
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
    optionsmenu.add_separator()
    
    tabs = tk.Menu(master, tearoff=0)
    tabs.add_checkbutton(label="Spaces for tabs",variable=master.master.spaces,
        command=master.master.updateTabStyle)
    tabs.add_checkbutton(label="Magic tabs",variable=master.master.magic,
        command=master.master.updateTabStyle)
    size = tk.Menu(tabs, tearoff=0)
    for i in range (9):
        size.add_radiobutton(label=str(i),variable=master.master.tabsize,value=i,
            command=master.master.updateTabStyle)
    tabs.add_cascade(label="Tab Size",menu=size)
    optionsmenu.add_cascade(label="Tab Options",menu=tabs)
    optionsmenu.add_separator()
    
    colormenu = tk.Menu(master,tearoff=0)
    
    colormenu.add_separator
    colormenu.add_radiobutton(label="White on Black",variable=master.master.predColors,
        value="WhiteOnBlack",command=master.master.colorPredefined)
    colormenu.add_radiobutton(label="Black on White",variable=master.master.predColors,
        value="BlackOnWhite",command=master.master.colorPredefined)
    colormenu.add_radiobutton(label="Green on Black",variable=master.master.predColors,
        value="GreenOnBlack",command=master.master.colorPredefined)
    colormenu.add_radiobutton(label="Scarlet and Grey",variable=master.master.predColors,
        value="ScarletOnGrey",command=master.master.colorPredefined)
    colormenu.add_radiobutton(label="White on Blue",variable=master.master.predColors,
        value="WhiteOnBlue",command=master.master.colorPredefined)
    colormenu.add_radiobutton(label="Yellow on Black",variable=master.master.predColors,
        value="YellowOnBlack",command=master.master.colorPredefined)
    colormenu.add_separator()
    colormenu.add_command(label="Custom Text Color",command=master.master.setTextColor)
    colormenu.add_command(label="Custom Background Color",
        command=master.master.setBackgroundColor)
    
    optionsmenu.add_cascade(label="Color Options",menu=colormenu)
    #optionsmenu.add_checkbutton(label="Line Numbers",variable=master.master.lines,
    #    command=master.master.lineNumbers)
    return optionsmenu
    
if __name__ == "__main__":
    print ("Menus is a library.")