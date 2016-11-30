from tkinter import *
import time

class App():
    def __init__(self):
        #Set up window variables
        self.window = Tk() 
        self.root = Frame(self.window, height=150,width=30)
        self.window.title('Blueberry Productivity')

        self.text = Text(self.window) #Main text window
        self.text.config(wrap=WORD)
        self.wcLabel = Label(text="",width=10)
        '''
        Basic variables
        '''
        self.wordCount = 0
        self.graphWidth = 200
        self.graphHeight = 220
        self.dayWC = [0]*31 #Day wordcount
        self.wkWC = [0]*8 #Week wordcount
        self.dayInterval = 1 #current interval for logging daily word count
        self.dayScale = self.graphWidth/len(self.dayWC)
        self.goal_dayWC = 100
        self.dayCounter = 60000
        self.wkInterval = 1 #current interval for logging weekly word count
        self.bg_color = "#B1D0D3"
        self.hl_color = "#46C4CF"
        self.window.config(bg=self.bg_color)
        '''
        Buttons
        '''
        #Goal Activation Button
        self.goalEdit = False
        self.button_makeGoal = Button(self.window, text = "   +   ", command=self.EnterGoal,state=NORMAL,bg=self.hl_color)
        #Reminder Activation Button
        self.remEdit = False
        self.button_makeRem = Button(self.window, text = "   )(   ", command=self.EnterRem,bg=self.hl_color)
        #Day Goal Enterance Box
        self.dayGoal_label = Label(self.window,text = "Daily Goal", bg=self.bg_color)
        self.dayGoalWC = Entry(self.window,bg=self.hl_color,disabledbackground=self.bg_color)
        self.dayGoalWC.insert(0,str(self.goal_dayWC))
        self.dayGoalWC.config(state=DISABLED)
        #Reminder Enterance Box
        self.rem1_label = Entry(self.window,bg=self.hl_color,disabledbackground=self.bg_color) #for what the reminder should say
        self.rem1_label.insert(0,"Enter reminder here.")
        self.rem1_label.config(state=DISABLED)
        self.rem1_Int = Entry(self.window,bg=self.hl_color,disabledbackground=self.bg_color) #When they want to be reminded (or in how long they want to be reminded)
        self.rem1_Int.insert(0,"Enter time (in minutes)")
        self.rem1_Int.config(state=DISABLED)
        '''
        Graphs
        '''
        #Daily
        self.dayGraph = Canvas(self.window,height=self.graphHeight,width=self.graphWidth)
        self.dayGraph.create_text(2,2,text="Daily Word Count",anchor="nw") #Graph label
        self.dayGraph.create_rectangle(2,20,self.graphWidth,self.graphHeight)#Make boarder
        '''
        Notification
        '''
        #Variables
        self.notif = Canvas(self.window, height=self.graphHeight/4, width=self.graphWidth)
        #self.notif.create_text(2,2,text = "Notification here",anchor="nw",tag="notifTag")
        self.notif.config(bg="#7EE2E4")
        
        '''
        Other dressy stuff
        '''
        self.fakeMenu = Label(self.window,text="File     Edit     View     Format     Help")
        self.fakeMenu.config(anchor="w")
        '''
        Pack everything in the grid
        '''
        #Main text Box
        self.text.grid(row=1,column=2,rowspan=15,columnspan=4)
        self.text.config(height=50)
        self.fakeMenu.grid(row=0,column=0,columnspan=7)
        #Right Margin
        self.button_makeGoal.grid(row=1,column=6,sticky=E) #Buttons
        self.button_makeRem.grid(row=1,column=7,sticky=W)
        self.dayGoalWC.grid(row=2,column=7) #Goal Boxes
        self.dayGoal_label.grid(row=2,column=6)
        self.rem1_label.grid(row=3,column=6,padx=3)#Reiminder Boxes
        self.rem1_Int.grid(row=3,column=7,padx=5)     
        #Left Margin
        self.notif.grid(row=1,column=0) 
        self.wcLabel.grid(row=1,column=1)
        self.dayGraph.grid(row=2,column=0,columnspan=2,rowspan=1)
        #Run through everything
        self.timerupdate()
        self.graphUpdate()
        self.notifiUpdate()
        self.root.mainloop()

    # Button functions to test if the button objects work and to analyze the entered text
    def TextAnalysis(self):
        self.wordCount = 0
        for word in self.text.get("1.0",END).split(" "):
            self.wordCount += 1
        return self.wordCount
        #messagebox.showinfo(None, wordCount)
    def EnterGoal(self):
        if self.goalEdit == False:
            self.goalEdit = True
            self.dayGoalWC.config(state=NORMAL)
        else:
            self.goalEdit = False
            self.dayGoalWC.config(state=DISABLED)
            self.goal_dayWC = int(self.dayGoalWC.get())
    def EnterRem(self):
        if self.remEdit == False:
            self.remEdit = True
            self.rem1_label.config(state=NORMAL)
            self.rem1_Int.config(state=NORMAL)
        else:
            self.remEdit = False
            self.rem1_label.config(state=DISABLED)
            self.rem1_Int.config(state=DISABLED)


    # Updater loob
    def timerupdate(self):
        self.TextAnalysis()
        self.wcLabel.configure(text=self.wordCount)
        self.dayWC[self.dayInterval] = self.wordCount
        self.root.after(100, self.timerupdate)
    def graphUpdate(self):
        if self.dayInterval < len(self.dayWC)-1:
            self.dayGraph.create_line((self.dayInterval-1)*self.dayScale,(1-(self.dayWC[self.dayInterval-1]/self.goal_dayWC))*self.graphHeight,self.dayInterval*(self.dayScale),(1-(self.dayWC[self.dayInterval]/self.goal_dayWC))*self.graphHeight,width=2)
            self.dayInterval += 1        
        self.root.after(self.dayCounter, self.graphUpdate)
    def notifiUpdate(self):
        if self.dayInterval >= len(self.dayWC)-1: #Did not make goal
            if self.wordCount < self.goal_dayWC:
                self.notif.delete("notifTag")
                self.notif.create_text(2,2,text = ":(",anchor="nw",tag="notifTag")
                self.notif.config(relief="ridge",bg="#7EE2E4",bd=1)
            else:
                self.notif.delete("notifTag")
                self.notif.create_text(2,2,text = ":)",anchor="nw",tag="notifTag")
                self.notif.config(relief="ridge",bg="#7EE2E4",bd=1)
        self.root.after(100, self.notifiUpdate)


app=App()
app.mainloop()