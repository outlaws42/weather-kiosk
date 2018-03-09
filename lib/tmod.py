#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import random
import os
import os.path
import sys
import inspect
import pickle
import datetime

try:
    from bs4 import BeautifulSoup  # Needs to be installed through pip
    import requests
except:
    pass
# File I/O /////////////////////////////////////////
def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(sys.argv[0])
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

def open_file(file_,type_='relative',variable='Hey'):
    home = os.path.expanduser("~")
    try:
        if type_ == 'home':
            with open('{}/{}'.format(home,file_), 'r') as path_text:
                variable=path_text.read()
        else:
            with open(get_resource_path(file_), 'r') as text:
                variable=text.read()
        return variable
    except(FileNotFoundError) as e:
        print(e)
        if type_ == 'home':
            with open('{}/{}'.format(home,file_), 'w') as output:
                output.write(variable)
        else:
            with open(get_resource_path(file_), 'w') as output:
                output.write(variable)

def save_file(file_,variable,type_='relative'):
    home = os.path.expanduser("~")
    if type_ == 'Home':
        with open('{}/{}'.format(home,file_), 'w') as output:
            output.write(variable)
    else:
        with open(get_resource_path(file_), 'w') as output:
            output.write(variable)

def save_pickle(file_,variable,type_='relative'):
    home = os.path.expanduser("~")
    try:
        if type_ == 'home':
            with open('{}/{}'.format(home,file_), 'wb') as fle:
                    pickle.dump(variable, fle)
        else:
            with open(get_resource_path(file_), 'wb') as fle:
                    pickle.dump(variable, fle)
                    print('saved file')
    except(FileNotFoundError) as e:
        print(e)
        
def open_pickle(file_,type_='relative'):
    home = os.path.expanduser("~")
    try:
        if type_ == 'home':
            with open('{}/{}'.format(home,file_), 'rb') as fle:
                    variable = pickle.load(fle)
            return variable
        else:
            with open(get_resource_path(file_), 'rb') as fle:
                    variable = pickle.load(fle)
            return variable
    except(FileNotFoundError, EOFError) as e:
        print(e)
        variable = 0
        if type_ == 'home':
            with open('{}/{}'.format(home,file_), 'wb') as fle:
                pickle.dump(variable, fle)
        else:
            with open(get_resource_path(file_), 'wb') as fle:
                pickle.dump(variable, fle)
              
# Gleen info ////////////////////////////////////////////////////
def html_info(tag,url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        find_status = soup.find(tag)
        final_status = find_status.text.strip()
    except requests.exceptions.RequestException as e:
        print(e)
        final_status = "Can't connect"
        print(final_status)
    return final_status

def dict_to_list(list_,dictionary_):
        # Convert dictionary to a list
        temp = []
        list_ = []
        for key, value in dictionary_.items():
            temp = [key,value]
            list_.append(temp)
        return list_.sort()

def group_list(list_, positions, start=0):
    """
    takes a list and groups them into sub list in the amount of positions
    """
    while start <= len(list_) - positions:
        yield list_[start:start + positions]
        start += positions

def random_list(list_):
    """
        Randomizes a list
    """
    for item in range(1):
        rand = random.sample(list_, len(list_))
    return rand

def reverse_sublist(self,list_):
    for i in range(0,len(list_),2):
        list_[i][:] = list_[i][::-1]
    return list_
    
# Date/Time//////////////////////////////////////////////
def day_diff(month,day,year):
    current = datetime.date.today()
    day = datetime.date(year,month,day)
    till_day = day - current
    return till_day.days
    
def year_current():
    current = datetime.date.today()
    current_year = current.year
    return current_year
    
def time_now():
    current =  datetime.datetime.now().time().strftime('%H:%M:%S')
    return current
