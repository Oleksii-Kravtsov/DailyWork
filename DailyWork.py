
from functools import partial
import tkinter as tk
from tkinter import *
import os

folderPath = os.path.dirname(os.path.abspath(__file__))
inputFileName = "DailyWorkFile.txt"
inputFilePath = os.path.join(folderPath, inputFileName)


#The main window
class custom( Frame):
    def __init__(self, parent):
        
        #loads the data from a file and puts it into the right variables
        def loadFile(loadData):
            nonlocal data
            nonlocal dataList
            nonlocal timeInputStartingText
            nonlocal repeatInputStartingText

            if not loadData == "":
                data = loadData
            else:
                return

            dataList = data.splitlines()
            try:
                firstLine = dataList[0]
                firstSemiIndex = firstLine.index(":")
                timeInputStartingText = firstLine[0:firstSemiIndex]
                repeatInputStartingText = firstLine[firstSemiIndex+1:len(firstLine)]
            except IndexError:
                return

        #saves the data
        def saveFile():
            nonlocal dataList
            file = open(inputFilePath, 'w')

            dataList[0] = "{}:{}".format(self.timeInput.get(),self.repeatInput.get())
            output = "\n".join(dataList)
            file.write(output)

        #closes the application and saves it in the process.
        def closeWindow():
            saveFile()
            parent.destroy()
            

        #method to save text for keybinds
        def enterText(event):
            submitUserInput()
            self.focus_set()
        
        #method that increases increment for the arrow keys. Accessed through keybinds.
        def enableTenIncrement(state, event):
            self.usingTenIncrement = state

        #method that submits user input to dataList and calls updater to change the Visual on the screen. 
        def submitUserInput():
            nonlocal dataList
            minutesStr = self.timeInput.get()
            timesMultiplierStr = self.repeatInput.get()
            try:
                minutes = int(minutesStr)
                timesMultiplier = int(timesMultiplierStr)
            except ValueError:
                return
            totalMinutes = minutes * timesMultiplier
            if(totalMinutes == 0):
                return
            if(totalMinutes % 60 > 0 and totalMinutes / 60 >= 1):
                output = "{} hours : {} minutes".format(int(totalMinutes/60), totalMinutes % 60)
            elif totalMinutes % 60 == 0:
                output = "{} hours".format(int(totalMinutes/60))
            else:
                output = "{} minutes".format(totalMinutes % 60)
            dataList.insert(1,output)
            print(totalMinutes, int(totalMinutes/60), totalMinutes%60, totalMinutes%60 > 0)
            updateVisualData()

        #method that updates the visual information on the screen.
        def updateVisualData():
            removeVisualData()
            for i in range(1, len(dataList)):
                label = Label(self, text = dataList[i], name= "label{}".format(i-1))
                button = Button(self, text="X", name= "button{}".format(i-1), command= partial(removeVisualDataRow,i-1))
                label.grid(row= i+5, column=0)
                button.grid(row=i+5, column=1, pady = 3)
                self.dataRows.append([label,button])

                

                
        #method the data from the screen
        def removeVisualData():
            for visualList in self.dataRows:
                for widget in visualList:
                    widget.destroy()
            self.dataRows.clear()

        #method that gives button the ability to remove the row in which they are located.
        def removeVisualDataRow(i):
            for widget in self.dataRows[i]:
                widget.destroy()
            self.dataRows.pop(i)
            dataList.pop(i+1)

            updateButtons()

        #update button to data row connections
        def updateButtons():
            for visualList in self.dataRows:
                a = 0
                for widget in visualList:
                    if(widget.winfo_name().find("button") != -1):
                        widget.configure(command= partial(removeVisualDataRow,a))

        def addEntryInput(addictive, name):
            if(self.usingTenIncrement):
                addictive *= 10
            widget = self.nametowidget(name)
            try:
                newNumber = int(widget.get()) + addictive
            except ValueError:
                return
            if(newNumber > 9*int("".ljust(widget.maxNumbersTyped,"1"))  or newNumber < 0):
                return
            widget.delete(0,len(widget.get()))
            widget.insert(0,newNumber)




        timeInputStartingText = "0"
        repeatInputStartingText = "0"
        data = "\n"
        dataList = [""]
        self.dataRows = []
        self.usingTenIncrement = False
        self.tenIncrementEnable = (enableTenIncrement)


        try:
            file = open(inputFilePath, 'r')
            loadFile(file.read())
            file.close()
        except FileNotFoundError:
            print("Save file not found")


        tk.Frame.__init__(self)
        self.pack(side=LEFT, pady= 10,padx= 10, anchor=NW)
        vcmd = (parent.register(self.validateInput))

        self.repeatInputArrowUp = Button(self, text = "⬆", width= 2, command= partial(addEntryInput, 1, "timeInput"))
        self.repeatInputArrowUp.grid(row= 0, column= 0)

        self.repeatInputArrowUp = Button(self, text = "⬇", width= 2, command= partial(addEntryInput, -1, "timeInput"))
        self.repeatInputArrowUp.grid(row= 2, column= 0)

        self.timeInputArrowUp = Button(self, text = "⬆", width= 2, command= partial(addEntryInput, 1, "repeatInput"))
        self.timeInputArrowUp.grid(row= 0, column= 1)

        self.timeInputArrowUp = Button(self, text = "⬇", width= 2, command= partial(addEntryInput, -1, "repeatInput"))
        self.timeInputArrowUp.grid(row= 2, column= 1)

        

        self.timeInput = Entry(self, width= 10, name="timeInput", validate= "key", validatecommand= (vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.timeInput.bind("<Return>" , enterText )
        self.timeInput.bind("<Escape>" , enterText, add = "+")
        self.timeInput.grid(row = 1, column= 0, pady = 7, padx = 5)
        self.timeInput.maxNumbersTyped = 3
        self.timeInput.insert(0, timeInputStartingText)

        self.repeatInput = Entry(self, width= 10, name="repeatInput", validate= "key", validatecommand= (vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.repeatInput.bind("<Return>" , enterText )
        self.repeatInput.bind("<Escape>" , enterText, add = "+")
        self.repeatInput.grid(row = 1, column= 1, padx = 5)
        self.repeatInput.maxNumbersTyped = 2
        self.repeatInput.insert(0, repeatInputStartingText)

        self.sumbitButton = Button(self, width= 10, text = "Submit", command= submitUserInput)
        self.sumbitButton.grid(row = 1, column= 2)





        updateVisualData()
        parent.protocol("WM_DELETE_WINDOW", closeWindow)
        #atexit.register(closeWindow, self.timeInput.get(),self.repeatInput.get()) 
        
    #makes sure that the input box is not bigger than specified.
    def validateInput(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        widget = self.nametowidget(widget_name)
        widgetName = widget.winfo_name()
        try:
            maxNumbersTyped = widget.maxNumbersTyped
        except AttributeError:
            print("AttributeError: no 'maxNumbersTyped' found in %s" % (widgetName))
            return
        
        if len(value_if_allowed) > maxNumbersTyped:
            return False
        if (text):
            try:
                inputInt =int(text)
                return True
            except ValueError:
                return False




def main():

    root = Tk()
    cust = custom(root)
    root.title("DailyWork")

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    windowWidth = screenHeight / 2 
    windowHeight = screenHeight / 2 
    xOffset =  screenWidth / 2 - windowWidth/2
    yOffset = screenHeight / 2 - windowHeight/2
    root.geometry("%dx%d+%d+%d" % (windowWidth,windowHeight,xOffset,yOffset))

    def positionOnScreen(event):
        print("key : %d,%d" % (event.x,event.y))
    root.bind('<Key-space>',positionOnScreen )

    root.bind("<KeyPress-Shift_L>", partial(cust.tenIncrementEnable,True))
    root.bind("<KeyRelease-Shift_L>", partial(cust.tenIncrementEnable,False))

    root.mainloop()


if __name__ == '__main__':
    main()