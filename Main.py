# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 12:41:44 2021

@author: Esin Ayyıldız
"""
from Tasks import Tasks

def main():
    task = Tasks()
    task.issues_new_graph()
    task.closed_graph()
    task.time_ent_graph()
    task.custom_field()
    task.gantt_chart()
    task.gui_time_new()
    task.gui_time_closed()
    
if __name__== "__main__" :
    main()
   
