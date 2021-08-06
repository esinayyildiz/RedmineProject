# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:53:27 2021

@author: Esin Ayyıldız

♥

☻

"""
from datetime import date
from os import name
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline.offline import plot
from six import b
from RedmineClient import RedmineClient 
from enum import Enum
import numpy as np
import plotly.express as px
import plotly.offline as plotly
from tkinter import *
import tkinter as tk
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import plotly.graph_objects as go
from itertools import cycle


class Tasks:
    
    redmine=RedmineClient()     
    
    def issues_new_graph(self):
        issues_get = self.redmine.issues_get()['issues']

        dates = list(map(lambda entry: entry['start_date'],issues_get))
        values = list(map(lambda entry: entry['id'],issues_get))

        df = pd.DataFrame({'dates':dates, 'values':values})
        df['dates']  = [pd.to_datetime(i) for i in df['dates']]

        plt.plot(dates, values,color="red",label="New") 
        plt.xlabel("Dates")
        plt.ylabel("Id of Issues")
        plt.title('The graph  of new issues')
        plt.legend()
        plt.show()


    def issues_closed_graph(self):
        get_closed_issues = self.redmine.get_closed_issues()['issues']

        dates = list(map(lambda entry: entry['start_date'],get_closed_issues))
        value_closed = list(map(lambda entry: entry['id'],get_closed_issues))
        df = pd.DataFrame({'dates':dates, 'values':value_closed})
        df['dates']  = [pd.to_datetime(i) for i in df['dates']]

        plt.plot(dates,value_closed, label="Closed")
        plt.xlabel("Dates")
        plt.ylabel("Id of Issues")
        plt.title('The graph of closed issues')
        plt.legend()
        plt.show()


    def new_and_closed_issues(self):
        get_closed_issues = self.redmine.get_closed_issues()['issues']
        issues_get = self.redmine.issues_get()['issues']

        dates = list(map(lambda entry: entry['start_date'],get_closed_issues))
        value_closed = list(map(lambda entry: entry['id'],get_closed_issues))
        values_new = list(map(lambda entry: entry['id'],issues_get))
        df = pd.DataFrame({'dates':dates, 'values':value_closed,'values':values_new})

        plt.plot(dates,value_closed, label="Closed")
        plt.plot(dates, values_new, label="New")
        print(dates)
        print(value_closed)
        print(values_new)
        plt.xlabel("Dates")
        plt.ylabel("Id of Issues")
        plt.title('The graph of new and closed issues')
        plt.legend()
        plt.show()


    #all issues of RestRedmine project
    def time_ent_graph(self):
        time_entries = self.redmine.time_ent()['time_entries']
        custom_field = self.redmine.custom_field()['issues']

        # functool.group_by()
        values = list(map(lambda entry: entry['id'], time_entries))
        spent_time = list(map(lambda entry: entry['hours'],time_entries))
        estimated_time = list(map(lambda entry: entry['estimated_hours'],custom_field)) 
        values.sort()
        x = np.arange(len(values))
        _, ax = plt.subplots()
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
        print(values)
        for val in values:
            custom_fields = val.get('custom_fields')
            if custom_fields:
                npi_fields = list(filter(lambda f: f.get('name') == 'NPI', custom_fields))
                if npi_fields:
                    val['NPI'] = NPI(npi_fields[0].get('value'))

        npi_positive = list(filter(lambda val: val.get('NPI') == NPI.ENABLED, values))
        positive_count = len(npi_positive)
        negative_count = len(values) - positive_count

        y = [positive_count,negative_count]
        labels =["Yes","No"]
        explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        plt.pie(y,labels=labels,  shadow = True,explode=explode,colors=["black","purple"])
        plt.legend()
        plt.title(" NPI ")
        plt.show()


    def gantt_chart(self):
        gantt_chart = self.redmine.gantt_chart()['issues']

        dates_start = list(map(lambda entry: entry['start_date'], gantt_chart))
        due_date = list(map(lambda entry: entry['due_date'], gantt_chart)) 
        issues = list(map(lambda entry: entry['id'], gantt_chart))
        assigned_to = list(map(lambda entry: entry['assigned_to']['name'],gantt_chart))

        df = pd.DataFrame({'dates_start':dates_start, 'issues':issues,'due_date':due_date,'assigned_to':assigned_to})
        print(df)

        fig = px.timeline(df, x_start="dates_start", x_end="due_date", y="issues",color="assigned_to",title="<b>GANTT CHART</b>")
        fig.update_yaxes(autorange="reversed",type='category')
        fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries")
        plotly.offline.plot(fig)

        
    def write_excel(self,df):
    
       df.to_excel('./excel_sheet.xlsx')

        
    def gui_time_new(self):
        issues_get = self.redmine.issues_get()['issues']

        dates = list(map(lambda entry: entry['start_date'], issues_get))
        values = list(map(lambda entry: entry['id'],issues_get))
               
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

        get_closed_issues = self.redmine.get_closed_issues()['issues'] 
        dates = list(map(lambda entry: entry['start_date'],get_closed_issues))
        values = list(map(lambda entry: entry['id'],get_closed_issues))

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


    def time_ent_plotly(self):
        time_entries = self.redmine.time_ent()['time_entries']
        custom_field = self.redmine.custom_field()['issues']

        id = list(map(lambda entry: entry['id'], custom_field))
        spent_time = list(map(lambda entry: entry['hours'],time_entries))
        estimated_time = list(map(lambda entry: entry['estimated_hours'],custom_field)) 
        project = list(map(lambda entry: entry['project']['name'],custom_field))
        id.sort()
        print(id)
        print(spent_time)
        print(estimated_time)
        df = pd.DataFrame({'id':id, 'spent_time':spent_time,'estimated_time':estimated_time})
        fig = px.bar(df,x=id,y= ["estimated_time","spent_time"],barmode='group',facet_col=project,
        labels=dict(x="id of issues", y="estimated falan"))
        fig.update_xaxes(type='category')

        fig.update_layout(
        title="Issues in Spent time and Estimated time graphics",

        yaxis_title="Estimated vs Spent Time",
        
        legend_title="Times", )
        fig.update_traces( marker_line_color='rgb(8,48,107)', marker_line_width=2.5)
                
        plotly.offline.plot(fig)

    def time_entry_mtlib(self):

        class NPI(str,Enum):
            purple = "purple"
            RestRedmine = "RestRedmine"
            RESTJSONProject = "RESTJSONProject"

        time_entries = self.redmine.time_ent()['time_entries']
        custom_field = self.redmine.custom_field()['issues']

        id = list(map(lambda entry: entry['id'], custom_field))
        spent_time = list(map(lambda entry: entry['hours'],time_entries))
        estimated_time = list(map(lambda entry: entry['estimated_hours'],custom_field)) 
        project = list(map(lambda entry: entry['project']['name'],custom_field))
        print(project)

        id.sort()
        x = np.arange(len(id))
        _, ax = plt.subplots()
        ax.bar(x+0.35/2,spent_time,width=0.35,color="pink",label="Spent Time")
        ax.bar(x-0.35/2,estimated_time,width=0.35,color="purple",label="Estimated Time")

        plt.ylabel("Hours")
        plt.xlabel("Id of Issues")
        ax.set_xticks(x)
        ax.set_xticklabels(id)

        for val in project:
            project = val.get('project') 
            npi_fields = list(filter(lambda f: f.get('name') == 'purple', project))
            if npi_fields:
                val['NPI'] = NPI(npi_fields[0].get('value'))   

        plt.legend()
        plt.show()





        