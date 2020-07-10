from tkinter import *
from tkinter.font import Font
import tkinter.ttk as ttk
import time, ctypes
try:
    from main import *
    from table import gettable
    print('Module loading completed')
except:
    ctypes.windll.user32.MessageBoxW(0,'Please check your internet connection','Internet Connection Error',0|0x10)
    quit()

class overview():

    def clear(self):

        try:
            self.total_cases_label.place_forget()
            self.total_death_label.place_forget()
            self.total_recovered_label.place_forget()
            self.frame1.place_forget()
            self.frame2.place_forget()
            self.frame3.place_forget()
            self.table.place_forget()
            self.tableheadingline.place_forget()
            [i.place_forget() for i in self.heading]
            self.tablevsb.place_forget()
        except:
            pass

    def __init__(self):

        global style, tabnow
        
        #initialize the font
        self.titlefont = Font(size=30, family='Bahnschrift SemiBold')
        self.cases_label_font = Font(size=60, family='Bahnschrift')
        #initialize all the variable
        self.frame1 = Frame(root, bg='#696969')
        self.frame2 = Frame(root, bg='#696969')
        self.frame3 = Frame(root, bg='#696969')
        self.cases_num = total_cases_num()
        self.total_cases_numm = int(self.cases_num[0].replace(' ', '').replace(',', ''))
        self.total_death_numm = int(self.cases_num[1].replace(' ', '').replace(',', ''))
        self.total_recovered_numm = int(self.cases_num[2].replace(' ', '').replace(',', ''))
        self.total_cases_num_title = Label(self.frame1, text='Total Cases', font=self.titlefont, bg='#696969', fg='white')
        self.death_num_title = Label(self.frame2, text='Total Deaths', font=self.titlefont, bg='#696969', fg='white')
        self.recovered_num_title = Label(self.frame3, text='Total Revovered', font=self.titlefont, bg='#696969', fg='white')
        self.total_cases_label = Label(self.frame1, text=self.total_cases_numm, font=self.cases_label_font, bg='#696969', fg='white')
        self.total_death_label = Label(self.frame2, text=self.total_death_numm, font=self.cases_label_font, bg='#696969', fg='white')
        self.total_recovered_label = Label(self.frame3, text=self.total_recovered_numm, font=self.cases_label_font, bg='#696969', fg='white')
        style.configure("Treeview", highlightthickness=0, rowheight=40, bd=0, font=('Bahnschrift', 15), background="#191919", fieldbackground="white", foreground="white") # Modify the font of the body
        style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        self.column_names = ("1", '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15')
        self.table = ttk.Treeview(root, column=self.column_names, style="Treeview", height=10, show="tree", selectmode='none')
        self.table.column('#0', width=0, minwidth=0, stretch=NO)
        self.table.column('1', width=50, minwidth=50, stretch=NO, anchor='e')
        self.table.column('2', width=200, minwidth=200, stretch=NO)
        [self.table.column(str(i), width=110, minwidth=110, stretch=NO, anchor='e') for i in range(3, 15)]
        self.table.column(15, width=130, minwidth=130, stretch=NO, anchor='e')
        self.header = ['No.', 'Country/\nOthers', 'Total\nCases', 'New\nCases', 'Total\nDeaths', 'New\nDeaths', 'Total\nRecovered', 'New\nRecovered', 'Active\nCases', 'Serious,\nCritical', 'Cases/\n1M pop', 'Deaths/\n1M pop', 'Total\nTests', 'Tests/\n1M pop', 'Population']
        self.heading = [Label(root, text=i, font=Font(size=15, family='Bahnschrift'), bg='#191919', fg='white', anchor='e', justify=RIGHT) for i in self.header]
        self.tableheadingline = Label(bg='#555555')
        self.coronatable = gettable()
        [self.table.insert("", END, values=[i+1]+['  '+str(a) for a in self.coronatable[i]]) for i in range(len(self.coronatable))]
        self.tablevsb = Scrollbar(root, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.tablevsb.set)

    def widget(self):

        global tabnow
        
        self.clear()
        app.cases.clear()
        app.cured.clear()
        app.death.clear()
        app.others.clear()
        
        #button_style_changing
        casesbtn.config(bg='#191919')
        curedbtn.config(bg='#191919')
        deathbtn.config(bg='#191919')
        otherbtn.config(bg='#191919')
        overviewbtn.config(bg='#696969')
        tabnow = overviewbtn

        #frame placing
        self.frame1.place(x=100, y=250, width=500, height=200)
        self.frame2.place(x=960, y=350, width=500, height=200, anchor='center')
        self.frame3.place(x=1820, y=450, width=500, height=200, anchor='se')

        #title placing
        self.total_cases_num_title.place(x=250, y=40, anchor='center')
        self.death_num_title.place(x=250, y=40, anchor='center')
        self.recovered_num_title.place(x=250, y=40, anchor='center')

        #number label placing
        self.total_death_label.place(x=250, y=120, anchor='center')
        self.total_recovered_label.place(x=250, y=120, anchor='center')
        self.total_cases_label.place(x=250, y=120, anchor='center')

        #table placing
        self.table.place(x=70, y=580)
        self.tablevsb.place(x=1800, y=590, height=380)
        self.tableheadingline.place(x=70, y=570, width=1780, height=2)
        self.heading[0].config(justify=LEFT)
        self.heading[1].config(justify=LEFT)
        self.heading[0].place(x=70, y=540)
        self.heading[1].place(x=130, y=515)
        self.x = 430
        for i in range(2, 14):
            self.heading[i].place(x=self.x, y=515, anchor='ne')
            self.x += 110
        self.heading[14].place(x=1770, y=540, anchor='ne')
    
class cases():

    def clear(self):

        try:
            [i.place_forget() for i in self.btnframe]
            self.total_button.place_forget()
            self.daily_button.place_forget()
            self.total_cases_chart.place_forget()
            self.daily_cases_chart.place_forget()
        except:
            pass

    def __init__(self):

        self.btnframe = [Frame(root, bg='#555555') for i in range(2)]

        self.btnfont = Font(size=20, family='Bahnschrift Condensed')
        self.total_button = Button(root, text='TOTAL', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        self.daily_button = Button(root, text='DAILY', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        self.total_cases_chart = total_cases_chart(root)
        self.daily_cases_chart = daily_cases_chart(root)

    def btn_on_enter(self, e):
        if e.widget != self.current_tab:
            e.widget['bg'] = '#696969'

    def btn_on_leave(self, e):
        if e.widget != self.current_tab:
            e.widget['bg'] = '#191919'

    def widget(self):

        def selfclear(self):
            try:
                self.total_cases.place_forget()
            except:
                pass
            try:
                self.daily_cases_chart.place_forget()
            except:
                pass

        def total_cases_tab(self):
            selfclear(self)
            self.total_cases_chart.place(x=960, y=600, anchor='center')
            self.total_button.config(bg='#696969')
            self.daily_button.config(bg='#191919')
            self.current_tab = self.total_button

        def daily_cases_tab(self):
            selfclear(self)
            self.daily_cases_chart.place(x=960, y=600, anchor='center')
            self.daily_button.config(bg='#696969')
            self.total_button.config(bg='#191919')
            self.current_tab = self.daily_button

        global tabnow

        self.clear()
        app.overview.clear()
        app.cured.clear()
        app.death.clear()
        app.others.clear()
        
        #button_style_changing
        casesbtn.config(bg='#696969', fg='white')
        overviewbtn.config(fg='white', bg='#191919')
        curedbtn.config(fg='white', bg='#191919')
        deathbtn.config(fg='white', bg='#191919')
        otherbtn.config(fg='white', bg='#191919')
        self.total_button.config(command=lambda: total_cases_tab(self))
        self.daily_button.config(command=lambda: daily_cases_tab(self))
        tabnow = casesbtn

        self.btnframe[0].place(x=98, y=218, width=834, height=64)
        self.btnframe[1].place(x=1822, y=218, width=834, height=64, anchor='ne')

        self.daily_button.place(x=1820, y=220, width=830, height=60, anchor='ne')
        self.total_button.place(x=100, y=220, width=830, height=60)

        total_cases_tab(self)

        [i.bind('<Enter>', self.btn_on_enter) for i in [self.total_button, self.daily_button]]
        [i.bind('<Leave>', self.btn_on_leave) for i in [self.total_button, self.daily_button]]

    
class cured():

    def clear(self):

        try:
            [i.place_forget() for i in self.btnframe]
            self.total_button.place_forget()
            self.daily_button.place_forget()
            self.total_cured_chart.place_forget()
            self.daily_cured_chart.place_forget()
        except:
            pass

    def __init__(self):

        self.btnframe = [Frame(root, bg='#555555') for i in range(2)]

        self.btnfont = Font(size=20, family='Bahnschrift Condensed')
        self.total_button = Button(root, text='TOTAL', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        self.daily_button = Button(root, text='DAILY', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        self.total_cured_chart = total_cured_chart(root)
        self.daily_cured_chart = daily_cured_chart(root)

    def btn_on_enter(self, e):
        if e.widget != self.current_tab:
            e.widget['bg'] = '#696969'

    def btn_on_leave(self, e):
        if e.widget != self.current_tab:
            e.widget['bg'] = '#191919'

    def widget(self):

        def selfclear(self):
            try:
                self.total_cured.place_forget()
            except:
                pass
            try:
                self.daily_cured_chart.place_forget()
            except:
                pass

        def total_cured_tab(self):
            selfclear(self)
            self.total_cured_chart.place(x=960, y=600, anchor='center')
            self.total_button.config(bg='#696969')
            self.daily_button.config(bg='#191919')
            self.current_tab = self.total_button

        def daily_cured_tab(self):
            selfclear(self)
            self.daily_cured_chart.place(x=960, y=600, anchor='center')
            self.daily_button.config(bg='#696969')
            self.total_button.config(bg='#191919')
            self.current_tab = self.daily_button

        global tabnow
        
        self.clear()
        app.overview.clear()
        app.cases.clear()
        app.death.clear()
        app.others.clear()
        
        #button_style_changing
        curedbtn.config(bg='#696969', fg='white')
        overviewbtn.config(fg='white', bg='#191919')
        casesbtn.config(fg='white', bg='#191919')
        deathbtn.config(fg='white', bg='#191919')
        otherbtn.config(fg='white', bg='#191919')
        self.total_button.config(command=lambda: total_cured_tab(self))
        self.daily_button.config(command=lambda: daily_cured_tab(self))
        tabnow = curedbtn

        self.btnframe[0].place(x=98, y=218, width=834, height=64)
        self.btnframe[1].place(x=1822, y=218, width=834, height=64, anchor='ne')

        self.daily_button.place(x=1820, y=220, width=830, height=60, anchor='ne')
        self.total_button.place(x=100, y=220, width=830, height=60)

        total_cured_tab(self)

        [i.bind('<Enter>', self.btn_on_enter) for i in [self.total_button, self.daily_button]]
        [i.bind('<Leave>', self.btn_on_leave) for i in [self.total_button, self.daily_button]]
    
class death():

    def clear(self):
        
        pass

    def __init__(self):
        
        pass

    def widget(self):

        global tabnow

        self.clear()
        app.cured.clear()
        app.cases.clear()
        app.overview.clear()
        app.others.clear()
        #button_style_changing
        overviewbtn.config(fg='white', bg='#191919')
        casesbtn.config(fg='white', bg='#191919')
        curedbtn.config(fg='white', bg='#191919')
        deathbtn.config(bg='#696969', fg='white')
        otherbtn.config(fg='white', bg='#191919')
        tabnow = deathbtn
    
class others():

    def clear(self):
        
        pass

    def __init__(self):

        pass

    def widget(self):

        global tabnow

        self.clear()
        app.overview.clear()
        app.cases.clear()
        app.cured.clear()
        app.death.clear()
        app.others.clear()
        #button_style_changing
        overviewbtn.config(fg='white', bg='#191919')
        casesbtn.config(fg='white', bg='#191919')
        curedbtn.config(fg='white', bg='#191919')
        deathbtn.config(fg='white', bg='#191919')
        otherbtn.config(bg='#696969', fg='white')
        tabnow = otherbtn

class main():

    def __init__(self):

        global root, overviewbtn, casesbtn, curedbtn, deathbtn, otherbtn, overviews, cureds, casess, deaths, otherss, style, app

        #initialize font
        self.btnfont = Font(size=20, family='Bahnschrift Condensed')

        style = ttk.Style()

        def fixed_map(option):
            return [elm for elm in style.map("Treeview", query_opt=option)
                    if elm[:2] != ("!disabled", "!selected")]

        style.map("Treeview",
                  foreground=fixed_map("foreground"),
                  background=fixed_map("background"))

        #initialize widget
        self.title = Label(root, text='COVID-19 DATA ANALYSIS', font=Font(size=30, family='Bahnschrift Condensed'), bg='#191919', fg='white')
        self.line = Label(bg='#555555')
        self.btnfrm = [Frame(root, bg='#555555') for i in range(5)]
        overviewbtn = Button(root, text='OVERVIEW', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        casesbtn = Button(root, text='CASES', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        curedbtn = Button(root, text='CURED', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        deathbtn = Button(root, text='DEATH', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)
        otherbtn = Button(root, text='OTHERS', font=self.btnfont, relief=FLAT, fg='white', bg='#191919', activebackground='#696969', activeforeground='white', borderwidth=0)

        #call the function and dump them into a variable respectively
        self.overview = overview()
        self.cases = cases()
        self.cured = cured()
        self.death = death()
        self.others = others()

        #call the overviews variable once when start the app

        #dump the variable into button command respectively
        overviewbtn.config(command=self.overview.widget)
        casesbtn.config(command=self.cases.widget)
        curedbtn.config(command=self.cured.widget)
        deathbtn.config(command=self.death.widget)
        otherbtn.config(command=self.others.widget)

    def button_on_enter(self, e):

            if e.widget != tabnow  and e.widget in [overviewbtn, casesbtn, curedbtn, deathbtn, otherbtn]:
                e.widget['bg'] = '#696969'
                root.update()
 
    def button_on_leave(self, e):

        if e.widget != tabnow and e.widget in [overviewbtn, casesbtn, curedbtn, deathbtn, otherbtn]:
            e.widget['bg'] = '#191919'
            root.update()


    def widget(self):

        self.overview.widget()

        #place the header
        self.title.place(x=950, y=40, anchor='center')
        self.line.place(x=960, y=80, height=2, width=1940, anchor='center')

        #place the tab button
        overviewbtn.place(x=100, y=120, width=300, height=60)
        casesbtn.place(x=455, y=120, width=300, height=60)
        curedbtn.place(x=960, y=150, width=300, height=60, anchor='center')
        deathbtn.place(x=1165, y=120, width=300, height=60)
        otherbtn.place(x=1820, y=120, width=300, height=60, anchor='ne')
        self.btnfrm[0].place(x=98, y=118, width=304, height=64)
        self.btnfrm[1].place(x=453, y=118, width=304, height=64)
        self.btnfrm[2].place(x=960, y=150, width=304, height=64, anchor='center')
        self.btnfrm[3].place(x=1163, y=118, width=304, height=64)
        self.btnfrm[4].place(x=1822, y=118, width=304, height=64, anchor='ne')

        root.bind('<Enter>', self.button_on_enter)
        root.bind('<Leave>', self.button_on_leave)

#will be useful in the future
'''
active_cases_chart = active_cases_chart(root)
infected_vs_recovered_chart = infected_vs_recovered_chart(root)
total_serious_and_critical_cases = total_serious_and_critical_cases(root)
outcome_of_total_close_cases = outcome_of_total_close_cases(root)
total_death_chart = total_death_chart(root)
daily_death_chart = daily_death_chart(root)
distribution_of_cases = distribution_of_cases(root)
distribution_of_cases.place(x=0, y=0, width=1200, height=700)
'''

root = Tk()
root.geometry('1920x1080')
root.config(bg='#191919')
root.title('Covid-19 Data Analysis')
root.state('zoomed')

app = main()
app.widget()

root.mainloop()
