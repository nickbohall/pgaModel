#Import scraping modules
from bs4 import BeautifulSoup
import requests
import scrapy
import json

#Import data manipulation modules
import pandas as pd
import numpy as np

def courses(): #helper function to get all of the courses & their numbers
    url = 'https://datagolf.com/course-history-tool'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    courses = soup.find('div', class_='dropdown-menu dropdown-menu-page dropdown-menu-left').find_all('button', class_='dropdown-item drop-item-page-course')
    courseDict = []
    for course in courses:
        tempDict = {'courseName': "", 'courseNumber': "", 'id': ""}
        course_name = course.text
        course_value = course['value']
        tempDict['courseName'] = course_name
        tempDict['courseNumber'] = course_value
        courseDict.append(tempDict)
    return courseDict
def playerNames():

def courseNames(): #list all course names
    courseList = []
    for course in courses():
        courseList.append(course['courseName'])
    return courseList

def apiScrape(courseName, courseNum, minRounds, id='', playing=False ): #This is the function that actually goes to the API for each course & number
    url = f'https://api.datagolf.ca/dg-api/v1/get_ch_data?callback=callback&course_num=ch_{courseNum}&_={id}'
    html_text = requests.get(url).text #goes to the url
    soup = BeautifulSoup(html_text, 'lxml') #us BS to parse html
    body = soup.find('p').text.split('callback')[1][2:-3]
    split = body.split('}, ')[:-1]
    course_dict = []
    for ele in split:
        ele += '}'
        cdict = json.loads(ele)
        course_dict.append(cdict)

    df = pd.DataFrame.from_dict(course_dict) #dict to df
    df = df.rename(columns={'mean_sg': 'True SG', 'mean_res_sg': 'versus expectation','suggested_adjustment': 'experience','count': 'appearences'})
    if playing == True: #defaults to if they're currently playing in the tourney
        df = df[df['in_field'] == 1] 
    df = df[df['appearences'] >= minRounds]
    df = df.sort_values(by='True SG', ascending=False) #Sorting by True SG
    print(courseName)
    return df

def allCourses(playing=False, minRounds = 1): #Loops through all of the courses and generates a df from the api
    for course in courses():
        df = apiScrape(course['courseName'], course['courseNumber'],playing, minRounds)
        print(df)

def oneCourse(course, playing = False, minRounds = 0):
    i = None
    for sub in courses():
        if sub['courseName'] == course:
            i = sub    
    df = apiScrape(i['courseName'], i['courseNumber'],playing, minRounds)
    return df

df = apiScrape('Colonial Country Club','21',True,1)
print(oneCourse('St. Andrews GC (Old Course)', minRounds=1).head(50))


