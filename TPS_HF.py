from tkinter import *
import time
import random

class App():
    def __init__(self):
        #Set up window variables
        self.window = Tk() 
        self.root = Frame(self.window, height=150,width=30)
        self.window.title('Blueberry Productivity')

        self.text = Text(self.window) #Main text window
        self.text.config(wrap=WORD)
        self.wcLabel = Label(text="",width=100)
        '''
        Basic variables
        '''
        self.wordCount = 0
        self.graphWidth = 150
        self.graphHeight = 170
        self.dayWC = [0]*31 #Day wordcount               
        self.dayScale = self.graphWidth/len(self.dayWC)
        self.goal_dayWC = 500
        self.goal_wkWC = 3000
        self.goal_mthWC = 10000
        self.dayCounter = 5000
        self.dayInterval = 1 #current interval for logging daily word count
        self.wkInterval = 5 #current interval for logging weekly word count
        self.mthInterval = 2 
        self.bg_color = "#B1D0D3"
        self.hl_color = "#46C4CF"
        self.wht_blue = "#E7FDFF"
        self.window.config(bg=self.bg_color)
        self.wcLabel.config(bg = self.bg_color)
        self.mfCount = 12 #media feed counter(Rahul)
        self.mailCount = 10 #mail counter(Rahul)
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
        self.dayGraph = Canvas(self.window,height=self.graphHeight,width=self.graphWidth,bd=1,relief=GROOVE)
        self.dayGraph.create_text(3,3,text="Daily Word Count",font=("Courier",8,"underline"),anchor="nw") #Graph label
        self.dayGraph.create_text(4,22,text=str(self.goal_dayWC-self.wordCount) + " to go",anchor="nw",tag="udDayWC")
        #Weekly (prepopulated)
        self.wkWC = [0,400,735,993,1320,1320] #Week wordcount (up to Thursday; test Friday)
        self.wkGraph = Canvas(self.window,height=self.graphHeight,width=self.graphWidth,bd=1,relief=GROOVE)
        self.wkGraph.create_text(3,3,text="Weekly Word Count",font=("Courier",8,"underline"),anchor="nw") #Graph label
        #self.wkGraph.create_rectangle(2,20,self.graphWidth,self.graphHeight)#Make boarder
        self.wkGraph.create_text(4,22,text=str(self.goal_wkWC-(self.wkWC[3]+self.wordCount))+" to go",anchor="nw",tag="udWkWC")
        self.wkScale = self.graphWidth/7
        #Monthly (prepopulated)
        self.mthWC = [0,1320,1320] #Week wordcount (up to Thursday; test Friday)
        self.mthGraph = Canvas(self.window,height=self.graphHeight,width=self.graphWidth,bd=1,relief=GROOVE)
        self.mthGraph.create_text(3,3,text="Monthly Word Count",font=("Courier",8,"underline"),anchor="nw") #Graph label
        self.mthGraph.create_text(4,22,text=str(self.goal_wkWC-(self.wkWC[3]+self.wordCount))+" to go",anchor="nw",tag="udMthWC")
        self.mthScale = self.graphWidth/30
        self.currentGraphHeight = self.mthGraph.winfo_height()

        '''
        Widgets
        '''
        #Media Feed
        self.mediaFeed_list = ["Johhny Appleseed: Ready for a big weekend.","CNN: Markets respond to recent events",
                               "Megan Smith: That new WW episode! WHAT!", "Chad Johnson: High Desert anyone?", "ESPN: College football teams prepare for playoffs.",
                               "CNN: Travel spending up from last holiday season.", "Stan Marsh: Feeling like a Harry Potter movie marathon.",
                               "Jami Times: Posted a new picture.", "Jeff Dean: Shared a link.","Jack Greenman: Damn you finals...damn you...",
                               "CNN: Experts debate the use of polls","CNN: Scientist continue work to combat Zika virus."]
        self.mediaFeed = Canvas(self.window,height=self.graphHeight,width=self.graphWidth)
        self.mediaFeed.config(bg=self.wht_blue,relief=SUNKEN,bd=1)
        self.mediaFeed.create_rectangle(0,0,self.graphWidth+4,20,fill=self.hl_color)
        self.mediaFeed.create_text(4,3,text="Media Feed",font=("Courier",10),anchor="nw")
        #Appointments
        self.cal = Canvas(self.window,height=self.graphHeight,width=self.graphWidth)
        self.cal.config(bg=self.wht_blue,relief=GROOVE,bd=1)
        self.cal.create_rectangle(0,0,self.graphWidth+4,20,fill=self.hl_color)
        self.cal.create_text(4,3,text="Calendar",font=("Courier",10),anchor="nw")
        self.cal.create_text(4,20,text = "All day - Jami's Birthday \n 11:35am - Class \n 2:00pm - Meeting with Tim \n 5:00pm - Paper due",anchor="nw")
        #Email(Rahul)
        self.email_list = ["Robin Mayers: 'You are qualified'", "Joe Philip: 'Meeting as per schedule'",
                           "Student Recruiter: 'Army Installation Management Command is hiring near you'",
                           "Amazon.com: 'Cyber Monday - Last chance for today's deals'", "Google: 'Your recovery phone number changed'",
                           "Arryn Robbins: 'Last GSC Meeting tomorrow at 5pm'", "Nelson Nwaogu: 'Request for Appointment'",
                           "Facebook: 'John Layfield commented on your post'", "CheapOAir: 'AIR TICKET NUMBER & AIRLINE CONFIRMATION. Booking# 35511345'",
                           "Jame Alexander: 'Flight got delayed'"]
        self.email = Canvas(self.window, height=self.graphHeight, width=self.graphWidth)
        self.email.config(bg=self.wht_blue, relief=SUNKEN, bd=1)
        self.email.create_rectangle(0, 0, self.graphWidth + 4, 20, fill=self.hl_color)
        self.email.create_text(4, 3, text="Email", font=("Courier", 10), anchor="nw")        

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
        self.fakeMenu.config(anchor="w",bg=self.bg_color)
        '''
        Pack everything in the grid
        '''
        #Main text Box
        self.text.grid(row=1,column=3,rowspan=15,columnspan=4)
        self.text.config(height=40)#Update that shit
        self.fakeMenu.grid(row=0,column=0,columnspan=8)
        self.wcLabel.grid(row=18,column=0,columnspan=8)
        #Right Margin
        self.button_makeGoal.grid(row=1,column=7,sticky=E) #Buttons
        self.button_makeRem.grid(row=1,column=8,sticky=W)
        self.dayGoalWC.grid(row=2,column=8) #Goal Boxes
        self.dayGoal_label.grid(row=2,column=7)
        self.rem1_label.grid(row=3,column=7,padx=3)#Reiminder Boxes
        self.rem1_Int.grid(row=3,column=8,padx=5)     
        #Left Margin
        self.notif.grid(row=1,column=0,columnspan=2) 
        self.dayGraph.grid(row=2,column=1,columnspan=2,rowspan=1)#***Change rowspan to 1 to get the widgets to full height. Why? Who the fuck knows?
        #self.mediaFeed.grid(row=5,column=1,columnspan=2,rowspan=1)
        #self.email.grid(row=5,column=1,columnspan=2,rowspan=1)
        self.cal.grid(row=5,column=1,columnspan=2,rowspan=1)
        #self.wkGraph.grid(row=8,column=1,columnspan=2,rowspan=1)
        self.mthGraph.grid(row=8,column=1,columnspan=2,rowspan=1)

        #Run through everything
        self.timerupdate()
        self.graphUpdate()
        self.notifiUpdate()
        self.mediaFeedUpdate()
        self.emailUpdate()
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
    '''
    Updaters
    '''
    def timerupdate(self):
        self.TextAnalysis()
        self.wcLabel.configure(text="Word Count: " + str(self.wordCount))
        self.dayWC[self.dayInterval] = self.wordCount 
        self.wkWC[self.wkInterval] = self.wordCount+self.wkWC[self.wkInterval-1]
        self.mthWC[self.mthInterval] = self.wordCount+self.mthWC[self.mthInterval-1]
        self.root.after(100, self.timerupdate)
    def graphUpdate(self):
        #update day graph
        self.currentGraphHeight = self.dayGraph.winfo_height()      
        if self.dayInterval < len(self.dayWC)-1:            
            self.dayGraph.delete("udDayLine")
            for i in range(0,self.dayInterval):
                self.dayGraph.create_line((i)*self.dayScale,(1-(self.dayWC[i]/self.goal_dayWC))*self.currentGraphHeight,(i+1)*(self.dayScale),(1-(self.dayWC[i+1]/self.goal_dayWC))*self.currentGraphHeight,width=2,tag="udDayLine")
        self.dayInterval += 1
        self.dayGraph.delete("udDayWC")
        self.dayGraph.create_text(4,22,text=str(self.goal_dayWC-self.wordCount)  + " to go",anchor="nw",tag="udDayWC")
        #update week graph
        self.currentGraphHeight = self.dayGraph.winfo_height()
        self.wkGraph.delete("udWkLine")
        self.wkGraph.delete("udWkWC")
        self.wkGraph.delete("wkLineBack")
        for i in range(0,len(self.wkWC)-1):
            self.wkGraph.create_line(i*self.wkScale,(1-(self.wkWC[i]/self.goal_wkWC))*self.currentGraphHeight,(i+1)*(self.wkScale),(1-(self.wkWC[i+1]/self.goal_wkWC))*self.currentGraphHeight,width=2,tag="wkLineBack")
        self.wkGraph.create_text(4,22,text=str(self.goal_wkWC-(self.wkWC[self.wkInterval]+self.wordCount))+" to go",anchor="nw",tag="udWkWC")       

        #update month graph
        self.currentGraphHeight = self.mthGraph.winfo_height()
        self.mthGraph.delete("udMthLine")
        self.mthGraph.delete("udMthWC")
        self.mthGraph.delete("mthLineBack")
        for i in range(0,len(self.mthWC)-1):
            self.mthGraph.create_line(i*self.mthScale,(1-(self.mthWC[i]/self.goal_mthWC))*self.currentGraphHeight,(i+1)*(self.mthScale),(1-(self.mthWC[i+1]/self.goal_mthWC))*self.currentGraphHeight,width=2,tag="mthLineBack")
        self.mthGraph.create_text(4,22,text=str(self.goal_mthWC-(self.mthWC[self.mthInterval]+self.wordCount))+" to go",anchor="nw",tag="udMthWC")     
   
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
    def mediaFeedUpdate(self):
        # update Media Feed ~ Rahul
        if self.mfCount > 0:
            self.mediaFeed.delete("mfnum")
            self.mediaFeed.create_text(4,22,text=str(self.mediaFeed_list[self.mfCount-1]),font=("Arial",7),anchor="nw",tag="mfnum")
            self.mediaFeed.create_text(4,46,text=str(self.mediaFeed_list[self.mfCount-2]),font=("Arial",7),anchor="nw",tag="mfnum")
            self.mediaFeed.create_text(4,68,text=str(self.mediaFeed_list[self.mfCount-3]),font=("Arial",7),anchor="nw",tag="mfnum")
            self.mediaFeed.create_text(4,90,text=str(self.mediaFeed_list[self.mfCount-4]),font=("Arial",7),anchor="nw",tag="mfnum")
            self.mfCount -= 1
            if self.mfCount == 0:
                #loop is repeating even after the set of notifications
                self.mfCount = 12
        self.root.after(10000, self.mediaFeedUpdate)
    def emailUpdate(self):
        # update Email ~ Rahul
        if self.mailCount > 0:
            self.email.delete("mailnum")
            self.email.create_text(4, 22, text=str(self.email_list[self.mailCount - 1]), font=("Arial", 7), anchor="nw", tag="mailnum")
            self.email.create_text(4, 46, text=str(self.email_list[self.mailCount - 2]), font=("Arial", 7), anchor="nw", tag="mailnum")
            self.email.create_text(4, 68, text=str(self.email_list[self.mailCount - 3]), font=("Arial", 7), anchor="nw", tag="mailnum")
            self.email.create_text(4, 90, text=str(self.email_list[self.mailCount - 4]), font=("Arial", 7), anchor="nw", tag="mailnum")
            self.mailCount -= 1
            if self.mailCount == 0:
                # loop is repeating even after the set of notifications
                self.mailCount = 10
        self.root.after(10000, self.emailUpdate)


app=App()
app.mainloop()
