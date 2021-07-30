# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:53:27 2021

@author: Esin Ayyıldız

♥

☻


"""
import pandas as pd
import matplotlib.pyplot as plt
from RedmineClient import RedmineClient 
from enum import Enum
import numpy as np
import plotly.express as px
import plotly.offline as plotly


class Tasks:
    
    redmine=RedmineClient()     
    
    def issues_get_graph(self):
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
        
        
    def time_ent_graph_person(self):
        values = [i['id'] for i in self.redmine.time_ent_person()['issues']] 
        spent_time = [i['hours'] for i in self.redmine.time_ent()['time_entries']]
        estimated_time = [i['estimated_hours'] for i in self.redmine.time_ent_person()['issues']]
        print(estimated_time)
        print(spent_time)
        print(values)
        values.sort()
        x = np.arange(len(values))
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(x+0.35/2,spent_time,width=0.35,color="black",label="Spent Time")
        ax.bar(x-0.35/2,estimated_time,width=0.35,color="red",label="Estimated Time")
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

        for i in range(len(values)):
           
            result=values[i]['custom_fields']

            print(result)
            
                
    
        
        enum_list = list(map(int, NPI))
        print(enum_list)


    def gantt_chart(self):
        dates_start = [i['start_date'] for i in self.redmine.gantt_chart()['issues']]
        due_date = [i['due_date'] for i in self.redmine.gantt_chart()['issues']]
        issues = [i['id'] for i in self.redmine.gantt_chart()['issues']]
        assigned_to= [i['assigned_to']['name'] for i in self.redmine.gantt_chart()['issues']]
  
        df = pd.DataFrame({'dates_start':dates_start, 'issues':issues,'due_date':due_date,'assigned_to':assigned_to})
        df['dates_start']  = [pd.to_datetime(i) for i in df['dates_start']]
        df['due_date']  = [pd.to_datetime(i) for i in df['due_date']]
        
        print(df)
        fig = px.timeline(df, x_start="dates_start", x_end="due_date", y="issues",color="assigned_to",title="<b>GANTT CHART</b>",opacity=0.7)
        fig.update_yaxes(autorange="reversed",type='category')

        
        

        plotly.offline.plot(fig)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        