# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:53:27 2021

@author: Esin Ayyıldız

♥

☻

"""
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline.offline import plot
from RedmineClient import RedmineClient 
from enum import Enum
import numpy as np
import plotly.express as px
import plotly.offline as plotly
from datetime import datetime, timedelta
import requests
from tkinter import *
import tkinter as tk
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


class Tasks:
    
    redmine=RedmineClient()     
    
    def issues_new_graph(self):
        dates = [i['start_date'] for i in self.redmine.issues_get()['issues']]
        values = [i['id'] for i in self.redmine.issues_get()['issues']]
        df = pd.DataFrame({'dates':dates, 'values':values})
        df['dates']  = [pd.to_datetime(i) for i in df['dates']]
        plt.plot(dates, values,color="red",label="New") 
        plt.xlabel("Dates")
        plt.ylabel("Number of Issues")
        plt.legend()
        plt.show()
        plt.plot(dates, range(len(values)),  label="New",marker='.',markerfacecolor="black", color='red', markersize=12)
        plt.xlabel("Dates")
        plt.ylabel("Number of Issues")
        plt.legend()


    def closed_graph(self):
        dates = [i['start_date'] for i in self.redmine.get_closed_issues()['issues']]
        values = [i['id'] for i in self.redmine.get_closed_issues()['issues']]
        df = pd.DataFrame({'dates':dates, 'values':values})
        df['dates']  = [pd.to_datetime(i) for i in df['dates']]
        plt.plot(dates,values, label="Closed",marker='.',markerfacecolor="red", color='black', markersize=12)
        plt.xlabel("Dates")
        plt.ylabel("Number of Issues")
        plt.legend()
        plt.show()
        plt.plot(dates, range(len(values)),color="black",label="Closed")
        plt.xlabel("Dates")
        plt.ylabel("Number of Issues")
        plt.legend()
        plt.show()


    #all issues of RestRedmine project
    def time_ent_graph(self):
        values = [i['id'] for i in self.redmine.time_ent()['time_entries']] 
        spent_time = [i['hours'] for i in self.redmine.time_ent()['time_entries']]
        estimated_time = [i['estimated_hours'] for i in self.redmine.custom_field()['issues']]
        print(estimated_time)
        print(spent_time)
        print(values)
        values.sort()
        x = np.arange(len(values))
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(x+0.35/2,spent_time,width=0.35,color="pink",label="Spent Time")
        ax.bar(x-0.35/2,estimated_time,width=0.35,color="purple",label="Estimated Time")
        plt.ylabel("Hours")
        plt.xlabel("Id of Issues")
        ax.set_xticks(x)
        ax.set_xticklabels(values)
        plt.legend()
        plt.show()
  
                
    def custom_field(self):
        
        class NPI(str,Enum):
            ENABLED = "1"
            DISABLED = "0"

        values = self.redmine.custom_field()['issues']
    
        for i in range(len(values)):
           
            result=values[i]['custom_fields']
        sample_list=[]

        for i in result:
            sample_list.append(i)

        print(sample_list)
        enum_list = list(map(int, NPI))

       
    def gantt_chart(self):
        dates_start = [i['start_date'] for i in self.redmine.gantt_chart()['issues']]
        due_date = [i['due_date'] for i in self.redmine.gantt_chart()['issues']]
        issues = [i['id'] for i in self.redmine.gantt_chart()['issues']]
        assigned_to= [i['assigned_to']['name'] for i in self.redmine.gantt_chart()['issues']]
        df = pd.DataFrame({'dates_start':dates_start, 'issues':issues,'due_date':due_date,'assigned_to':assigned_to})
        print(df)
        fig = px.timeline(df, x_start="dates_start", x_end="due_date", y="issues",color="assigned_to",title="<b>GANTT CHART</b>")
        fig.update_yaxes(autorange="reversed",type='category')
        fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries")
        plotly.offline.plot(fig)

        
    def write_excel(self,df):
    
       df.to_excel('./excel_sheet.xlsx')

        
    def gui_time_new(self):
        dates = [i['start_date'] for i in self.redmine.issues_get()['issues']]
        values = [i['id'] for i in self.redmine.issues_get()['issues']]
        df = pd.DataFrame({'dates':dates, 'values':values})
        fig = Figure(dpi = 120)
        plot1 = fig.add_subplot(111)
        plot1.set_ylabel('Id of Issues')
        plot1.set_xlabel('Dates')
        t0 = plot1.plot(dates, values,color="red",label="new issues")
        leg = plot1.legend(loc='upper right', fancybox=True, shadow=True)
        window = Tk()   
        canvas = FigureCanvasTkAgg(fig, master = window)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                   window)
        toolbar.update()
        canvas.get_tk_widget().pack()
        window.title('Plotting in Tkinter')
        window.geometry("800x650")
        plot_button = Button(master = window, 
                     height = 2, 
                     width = 10,command =self.write_excel(df),
                     text = "Excel Sheet"
                     )
        plot_button.pack()
        window.mainloop()


    def gui_time_closed(self):
        dates = [i['start_date'] for i in self.redmine.get_closed_issues()['issues']]
        values = [i['id'] for i in self.redmine.get_closed_issues()['issues']]
        df = pd.DataFrame({'dates':dates, 'values':values})
        fig = Figure(dpi = 120)
        plot1 = fig.add_subplot(111)
        plot1.set_ylabel('Id of Issues')
        plot1.set_xlabel('Dates')
        t0 = plot1.plot(dates, range(len(values)),color="black",label="closed issues")
        leg = plot1.legend(loc='upper right', fancybox=True, shadow=True)
        window = Tk()   
        canvas = FigureCanvasTkAgg(fig, master = window)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                   window)
        toolbar.update()
        canvas.get_tk_widget().pack()
        window.title('Plotting in Tkinter')
        window.geometry("800x650")
        plot_button = Button(master = window, 
                     height = 2, 
                     width = 10,command =self.write_excel(df),
                     text = "Excel Sheet"
                     )
        plot_button.pack()
        window.mainloop()

        