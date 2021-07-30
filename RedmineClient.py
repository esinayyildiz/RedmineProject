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
        url= f'{self.url}/time_entries.json?utf8=%E2%9C%93&set_filter=1&sort=spent_on%3Adesc&f%5B%5D=spent_on&op%5Bspent_on%5D=*&f%5B%5D=issue.status_id&op%5Bissue.status_id%5D=%3D&v%5Bissue.status_id%5D%5B%5D=1&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=hours&c%5B%5D=issue.status&group_by=&t%5B%5D=hours&t%5B%5D='
        return requests.get(url).json()
    
    
    def time_ent_person(self):
        url= f'{self.url}//projects/restredmine/issues.json?utf8=%E2%9C%93&set_filter=1&sort=id%3Adesc&f%5B%5D=status_id&op%5Bstatus_id%5D=o&f%5B%5D=&c%5B%5D=tracker&c%5B%5D=status&c%5B%5D=priority&c%5B%5D=subject&c%5B%5D=assigned_to&c%5B%5D=updated_on&c%5B%5D=cf_1&group_by=assigned_to&t%5B%5D='
        return requests.get(url).json()

    def custom_field(self):
        url= f'{self.url}/projects/restredmine/issues.json'
        return requests.get(url).json()
    
    
    def gantt_chart(self):
        url=f'{self.url}/projects/restredmine/issues.json'
        return requests.get(url).json()

    
    
        
        
        
        
        
        
    
    
        
  
