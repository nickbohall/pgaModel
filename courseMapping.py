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

def apiScrape(courseName, courseNum, id=''): #This is the function that actually goes to the API for each course & number
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

    print(courseName)
    df = pd.DataFrame.from_dict(course_dict) #dict to df
    return df

# print(apiScrape('14', '1653426856474'))

def allCourses(): #Loops through all of the courses and generates a df from the api
    for course in courses():
        print(apiScrape(course['courseName'], course['courseNumber']))
        break

print(allCourses())
print(courses())
