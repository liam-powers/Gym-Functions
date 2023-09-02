#import sys
#from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW, Label, Entry, Button, StringVar, BOTH, ttk
from tkinter import *
import webbrowser
from tkcalendar import Calendar, DateEntry
from collections import defaultdict

class GymApp(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Gym Companion App")

        self.pages = {}
        self.weight = 0
        self.height = 0
        self.bmi = 0
        self.onerepmax = 0
        self.datecaloriedict = defaultdict(int)
        
        self.create_homepage()
        self.create_caloriepage()
        self.create_bmipage()
        self.create_onereppage()
        self.create_linkpage()
        
        self.dcgrid = None
        self.bmidisplay = None
        self.oneRepOutput = None
        
        self.create_styles()
        self.show_page("homepage")
    
    def create_styles(self):
        buttons = ttk.Style()
        buttons.theme_use('alt')
        buttons.map("C.TButton",
                background=[("!active", "#EE2D37"), ('pressed', '!disabled', 'black'), ('active', '#c4232c')],
                cursor=[("active", "hand3")])
        buttons.configure("C.TButton", padding=10, font = ("Mono Sans", 30), foreground="white")
        
        labels = ttk.Style()
        labels.theme_use('alt')
        labels.configure("C.TLabel", font = ("Mono Sans", 20), foreground="white", padding=5, background="#323231")
    
    def create_homepage(self):
        self.pages["homepage"] = Frame(self.parent)
        
        self.pages["homepage"].columnconfigure(0, weight=1)
        self.pages["homepage"].columnconfigure(1, weight=1)
        self.pages["homepage"].columnconfigure(2, weight=1)
        self.pages["homepage"].rowconfigure(0)
        self.pages["homepage"].rowconfigure(1)
        self.pages["homepage"].rowconfigure(2)
        self.pages["homepage"].rowconfigure(3)
        self.pages["homepage"].rowconfigure(4)

        prompt = ttk.Label(self.pages["homepage"], text="Welcome to the Gym Companion App!", style="C.TLabel").grid(row=0, column=0, columnspan=3)
        
        calorieMenuButton = ttk.Button(self.pages["homepage"], text="Calorie Calculator", style="C.TButton", command=lambda: self.show_page("caloriepage"))
        bmiMenuButton = ttk.Button(self.pages["homepage"], text="BMI Calculator", style="C.TButton", command=lambda: self.show_page("bmipage"))
        oneRepMenuButton = ttk.Button(self.pages["homepage"], text="One Rep Max Calculator", style="C.TButton", command=lambda: self.show_page("onereppage"))
        linkMenuButton = ttk.Button(self.pages["homepage"], text="Useful Gym Links", style="C.TButton", command=lambda: self.show_page("linkpage"))
        
        calorieMenuButton.grid(row=1, column=1, pady=10)
        bmiMenuButton.grid(row=2, column=1, pady=10)
        oneRepMenuButton.grid(row=3, column=1, pady=10)
        linkMenuButton.grid(row=4, column=1, pady=10)
  
    def create_caloriepage(self):
        self.pages["caloriepage"] = Frame(self.parent) 
        homebutton = ttk.Button(self.pages["caloriepage"], text="Home", style="C.TButton", command=lambda: self.show_page("homepage"))
        homebutton.pack(pady=10)

        def modify_calories(modifier):
            if modifier == "add":
                self.datecaloriedict[self.calendardateentry.get_date()] += int(self.calentry_sv.get())
            elif modifier == "subtract":
                self.datecaloriedict[self.calendardateentry.get_date()] -= int(self.calentry_sv.get())
        
            if self.dcgrid is not None:
                self.dcgrid.destroy()
                
            self.dcgrid = Frame(self.pages["caloriepage"])
            self.dcgrid.pack()
                
            r = 0
            for date, calories in self.datecaloriedict.items():
                x = ttk.Label(self.dcgrid, text=(date, calories), style="C.TLabel")
                x.grid(row=r,column=0)
                r += 1
    
    
        lb1 = ttk.Label(self.pages["caloriepage"], text="Track Calories", style="C.TLabel", font=("Mono Sans bold", 30), padding=10).pack()
        cal = ttk.Label(self.pages["caloriepage"], text='Cals to add or subtract: ', style="C.TLabel").pack()
        self.calentry_sv = StringVar()
        calentry = Entry(self.pages["caloriepage"], textvariable=self.calentry_sv)
        calentry.pack()
        caldate = ttk.Label(self.pages["caloriepage"], text="Enter the date you are tracking for:", style="C.TLabel").pack()
        self.calendardateentry = Calendar(self.pages["caloriepage"], selectmode="day", year=2023, month=8, day=13)
        self.calendardateentry.pack(pady=5)
        add = Button(self.pages["caloriepage"], text="+", command = lambda: modify_calories("add")).pack()
        subtract = Button(self.pages["caloriepage"], text="-", command = lambda: modify_calories("subtract")).pack()
        
        datecolumn = ttk.Label(self.pages["caloriepage"], text="", style="C.TLabel")
        datecolumn.pack()
        caloriecolumn = ttk.Label(self.pages["caloriepage"], text="", style="C.TLabel")
        caloriecolumn.pack()
        
        #Display grid with date:entries laid out in two columns
        #dclbl = Label(self.pages["caloriepage"], text="")
        #dclbl.pack()

    def create_bmipage(self):
        self.pages["bmipage"] = Frame(self.parent)
        homebutton = ttk.Button(self.pages["bmipage"], text="Home", style="C.TButton", command=lambda: self.show_page("homepage"))
        homebutton.pack(pady=10)   
             
        def calculate_bmi():
            self.height = int(heightEntry.get())
            self.weight = int(weightEntry.get())
            self.bmi = 703 * (self.weight / (self.height * self.height))
            bmiText = "Your BMI is: ", str(round(self.bmi, 1)) 
            
            if self.bmidisplay is not None:
                self.bmidisplay.destroy()
                           
            self.bmidisplay = ttk.Label(self.pages["bmipage"], text="".join(bmiText), style="C.TLabel")
            self.bmidisplay.pack()

        heightEntry = StringVar()
        weightEntry = StringVar()


        bmihead = ttk.Label(self.pages["bmipage"], text="Track BMI", style="C.TLabel", font=("Mono Sans bold", 30), padding=10).pack()
        bmiheightprompt = ttk.Label(self.pages["bmipage"], text="Enter your height (in inches): ", style="C.TLabel").pack()
        bhent = Entry(self.pages["bmipage"], textvariable=heightEntry).pack()
        bmiweightprompt = ttk.Label(self.pages["bmipage"], text="Enter your weight (in lbs): ", style="C.TLabel").pack()
        bwent = Entry(self.pages["bmipage"], textvariable=weightEntry).pack()
        calbutton = Button(self.pages["bmipage"], text="Calculate!", command=calculate_bmi).pack()


    def create_onereppage(self):
        self.pages["onereppage"] = Frame(self.parent)
        homebutton = ttk.Button(self.pages["onereppage"], text="Home", style="C.TButton", command=lambda: self.show_page("homepage"))
        homebutton.pack(pady=10)
        
        def set_onerep():
            exweightkg = int(orweight.get()) / 2.2
            self.onerepmax = round(2.2 * (exweightkg * (36 / (37 - int(orvol.get())))), 2)
            oneRepOutputText = "Your one rep max is: ", str(self.onerepmax)
            
            if self.oneRepOutput is not None:
                self.oneRepOutput.destroy()
            
            self.oneRepOutput = ttk.Label(self.pages["onereppage"], text="".join(oneRepOutputText), style="C.TLabel")
            self.oneRepOutput.pack()

        orweight = StringVar()
        orvol = StringVar()

        oneRepTitle = ttk.Label(self.pages["onereppage"], text="Calculate 1RM", style="C.TLabel", font=("Mono Sans bold", 30), padding=10).pack()
        oneRepWeightPrompt = ttk.Label(self.pages["onereppage"], text="Weight of exercise, in pounds:", style="C.TLabel").pack()
        owe = Entry(self.pages["onereppage"], textvariable=orweight).pack()
        oneRepRepPrompt = ttk.Label(self.pages["onereppage"], text="Number of reps performed:", style="C.TLabel").pack()
        ovl = Entry(self.pages["onereppage"], textvariable=orvol).pack()
        oneRepCalculateButton = Button(self.pages["onereppage"], text="Calculate!", command=set_onerep).pack()

    def create_linkpage(self):
        self.pages["linkpage"] = Frame(self.parent)
        homebutton = ttk.Button(self.pages["linkpage"], text="Home", style="C.TButton", command=lambda: self.show_page("homepage"))
        homebutton.pack(pady=10)
        
        def callback(url):
            webbrowser.open_new_tab(url)
        
        #Sticky this?
        lb4 = ttk.Label(self.pages["linkpage"], text="Useful Gym Reference Links", style="C.TLabel")
        lb4.pack()
        gl1 = ttk.Label(self.pages["linkpage"], text="RP Strength", style="C.TLabel", foreground="#3366CC", cursor="hand2")
        gl1.bind("<Button-1>", lambda e: callback("https://rpstrength.com/"))
        gl1.pack()
        gl2 = ttk.Label(self.pages["linkpage"], text="Jeff Nippard", style="C.TLabel", foreground="#3366CC", cursor="hand2")
        gl2.bind("<Button-1>", lambda e: callback("https://jeffnippard.com/"))
        gl2.pack()
        gl3 = ttk.Label(self.pages["linkpage"], text="Cronometer", foreground="#3366CC", style="C.TLabel", cursor="hand2")
        gl3.bind("<Button-1>", lambda e: callback("https://www.cronometer.com/"))
        gl3.pack()
        
    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

def main():
    root = Tk()
    root.geometry("700x700+200+200")
    
    app = GymApp(root)
    app.grid(row=0, column=0, sticky="nsew")  
    root.grid_rowconfigure(0, weight=1) 
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()


if __name__ == '__main__':
    main()