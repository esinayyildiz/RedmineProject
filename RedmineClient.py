# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:22:43 2021

@author: Esin Ayyıldız

"""

import requests


class RedmineClient:  
    
    
    url = 'http://localhost/redmine'
    headers = {
  'Authorization': 'Basic ZXNpbmF5eWlsZGl6OmVzaW5heXlsZHo='}
    
    
    def users_get(self):
        url = f'{self.url}/users.json'
        return requests.get(url).json()
    
    
    def users_post(self):
        url= f'{self.url}/users.json'
        payload = {'user':[
            {  
            'login': 'localhost2',     
            'firstname': 'merve',     
            'lastname': 'bella',    
            'mail': 'mervebella@yahoo.fr',       
            'password': 'mervemervmerv'}]
            }
    
        return requests.post(url,payload).json()
    
    
    def issues_get(self):
        url= f'{self.url}/issues.json?project_id=1'
        return requests.get(url).json() 
    
    
    def get_closed_issues(self):
        url= f'{self.url}/issues.json?status_id=closed&project_id=1'
        return requests.get(url).json()
    
    
    def time_ent(self):
        query_param = {
            "f[]" : "issue.status_id",
            "op[issue.status_id]" : "=",
            "v[issue.status_id][]" : "1",
    
        }  

        url= f'{self.url}/time_entries.json?'
        return requests.get(url,params=query_param).json()
    
    
    def time_ent_person(self):
        params = {
            'f[]':"f[]",
            "op[status_id]" : "o",
            "f[]" : "",
            "c[]" : "status",
            "c[]" : "priority",
            "c[]" : "assigned_to",
            "group_by" : "assigned_to",
            "t[]" : ""


        }
        
        url= f'{self.url}/projects/restredmine/issues.json?'
        return requests.get(url, params=params).json()

    def custom_field(self):
        url= f'{self.url}/issues.json'
        return requests.get(url).json()
    
    
    def gantt_chart(self):
        url=f'{self.url}/projects/restredmine/issues.json'
        return requests.get(url).json()

    def excel(self):
        url = f'{self.url}/projects/restredmine/issues.json'
        return requests.get(url).json()

        
        
        
        
        
        
    
    
        
  
