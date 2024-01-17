#Step – 1(import necessary library)

# Message Box

from flask import (Flask, flash, redirect, render_template, request, session, abort,send_file,send_from_directory)
import pyodbc 
#from datetime import date
import pandas as pd
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import os
from multiprocessing import Process
from threading import Thread
from pymysql import*
import xlwt
import pandas.io.sql as sql
from flask import jsonify
#
from datetime import date
import math

def driverget():
    options = Options()
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
    chromeDriverFilePath = os.path.join(ROOT_DIR,'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #,chrome_options=options
    driver = webdriver.Chrome(executable_path=chromeDriverFilePath)
    return driver


def dbconnect():
    mydb = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=database-3.c1tcw6ocvqyh.us-east-1.rds.amazonaws.com;"
                        "Database=damo;"
                        "uid=Damo;pwd=Damo2021")
    return mydb

def Neededinputs(webid,webname):
    mydb = dbconnect()
    cursor = mydb.cursor()
    cursor.execute("select section_id from schema_mapping_data where id =? ",webid)
    Value1 = cursor.fetchone()
    sid = Value1.section_id
    cursor.execute("Select section_name from schema_mapping_data where id =?",webid)
    Value2 = cursor.fetchone()
    sname = Value2.section_name
    mydb = dbconnect()

    cursor1 = mydb.cursor()
    cursor1.execute("select latest_article_title from schema_mapping_data where section_name = '" +webname+"'")
    webname_point = cursor1.fetchone()
    current_article_heading = webname_point[0]
    print(current_article_heading)
    mydb.close()


    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("select id from [" +webname+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
    webid_point = cursor1.fetchone()
    current_aricle_id = webid_point[0]
    Count = int(current_aricle_id)

    return sid,sname,current_article_heading,Count

def Scrape(URL,heading,text,date,sid,sname,Count,webname,current_article_heading,call):
    driver = driverget()
    driver.get(URL)
    driver.maximize_window()
    time.sleep(6)
    try:
        driver.find_element_by_id('stat-modal-close').click()
    except:
        print('continue')
    try:
        Heading = driver.find_element_by_class_name(heading).text
    except:
        try:
            Heading = driver.find_element_by_id(heading).text
        except:
            try:
                Heading = driver.find_element_by_xpath('//*[@id="block-nyp-theme-content"]/article/div[3]/div/div/div/h1').text
            except:
                try:
                    Heading = driver.find_element_by_xpath('//*[@id="news-detail"]/div/div/h1').text
                except:
                    try:
                        Heading = driver.find_element_by_xpath('//*[@id="post-27636"]/h1').text
                    except:
                        try:
                            Heading = driver.find_element_by_xpath('//*[@id="jump-content"]/article/section[1]/div/div/h1').text
                        except:
                            Heading = heading
    try:
        Text = driver.find_element_by_class_name(text).find_elements_by_tag_name('p')
        Text1 = []
        for p in Text:
            Text1.append(p.text)
            s = "."
            Text = s.join(Text1)
    except:
        Text = driver.find_elements_by_tag_name('p')
        Text1 = []
        for p in Text:
            Text1.append(p.text)
            s = "."
            Text = s.join(Text1)
    try:
        Date = driver.find_element_by_class_name(date).text
    except:
        try:
            Date = driver.find_element_by_xpath('//*[@id="post-27636"]/div[2]/span/abbr').text
        except:
            try:
                Date = driver.find_element_by_tag_name(date).text
            except:
                try:
                    Date = date
                except:
                    Date = ''

    Result = {}
    # Result['Website'] = Website
    Result['Heading'] = Heading
    Result['Text'] = Text
    Result['Date'] = Date
    Result['URL'] = URL

    driver.close()
    # return Result
    print(Heading)
    print(current_article_heading)
    print(str(Heading) == current_article_heading)
    if(str(Heading) == current_article_heading):
        print('ifff')
        call = call - 1
        return 0  
    else:
        print('elseeee')
        if call == 1:
            print('this is the latest article')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (Heading, webname))
            # cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (Heading, webname))
            mydb.commit()
            mydb.close()
        mydb = dbconnect()
        cursor = mydb.cursor()
        query1 = 'INSERT INTO ['+ webname +'](article_url,article_heading1,article_text,article_date_website,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?)'
        print(query1)
        val1 = (Result['URL'],Result['Heading'],Result['Text'],Result['Date'],sid,sname,sid + 'A' + str(Count))
        cursor.execute(query1, val1)
        mydb.commit()
        mydb.close()
def Main(MainURL,start,end,operator,logic_number,heading,text,date,urlclass,webname,webid):
    
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    for i in range(start,end,logic_number):
        driver = driverget()
        driver.get(MainURL+str(i))
        driver.maximize_window()
        time.sleep(10)
        elems1 = driver.find_elements_by_class_name(urlclass)
        l=[]
        try:
            print('try')
            for k in elems1:
                l.append(k.find_element_by_tag_name('a').get_attribute('href'))
        except:
            print('except')
            for b in elems1:
                l.append(b.get_attribute('href'))
        driver.close()
        # print(len(elems1))
        # print(len(l))
        print(l)
        for j in l:
            Count = Count + 1
            call = call + 1
            returnvalue = Scrape(j,heading,text,date,sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    return

def Main2(MainURL,start,end,operator,logic_number,heading,text,date,urlclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    time.sleep(2)
    for i in range(start,end,logic_number):
        driver = driverget()
        driver.get(MainURL)
        print('inside for')
        try:
            print('inside tel health try')
            driver.find_element_by_xpath('//*[@id="year"]/div/select/option['+str(i)+']').click()
        except:
            print('inside tel health except')
            driver.find_element_by_class_name('blog-banner')
        time.sleep(3)
        elems1 = driver.find_elements_by_class_name(urlclass)
        try:
            a_tag = []
            for k in elems1:
                a_tag.append(k.find_element_by_tag_name('a'))
                l=[]
                for b in a_tag:
                    l.append(b.get_attribute('href'))
        except:
            l=[]
            for b in elems1:
                l.append(b.get_attribute('href'))

        driver.close()
        for j in l:
            Count = Count + 1
            call = call + 1
            returnvalue = Scrape(j,heading,text,date,sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    return
    

def Direct(MainURL,heading,text,date,urlclass,section,webname,webid):
    driver = driverget()
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver.get(MainURL)
    time.sleep(3)
    elems1 = driver.find_element_by_class_name(section).find_elements_by_class_name(urlclass)
    l=[]
    try:
        print('try')
        a_tag = []
        for k in elems1:
            a_tag.append(k.find_element_by_tag_name('a'))
            for b in a_tag:
                l.append(b.get_attribute('href'))
    except:
        print('except')
        for b in elems1:
            l.append(b.get_attribute('href'))
    driver.close()
    print(len(l))
    for j in l:
        call = call + 1
        Count = Count + 1
        returnvalue = Scrape(j,heading,text,date,sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            break
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
    mydb.commit()
    mydb.close()
    return
def Main_General(MainURL,start,end,operator,logic_number,heading,text,date,url,section,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    for i in range(start,end,logic_number):
        driver = driverget()
        driver.get(MainURL+str(i))
        time.sleep(10)
        h=[]
        a=[]
        try:
            needed_section = driver.find_element_by_id(section)
        except:
            needed_section = driver.find_element_by_class_name(section)
        Heading_list = needed_section.find_elements_by_class_name(heading)
        anchor_list = needed_section.find_elements_by_class_name(url)
        for i in Heading_list:
            h.append(i.text)
        for i in anchor_list:
            try:
                print('a in try')
                a.append(i.find_element_by_tag_name('a').get_attribute('href'))
            except:
                print('a in except')
                a.append(i.get_attribute('href'))
        d = []
        date_list = needed_section.find_elements_by_class_name(date)
        for i in date_list:
            d.append(i.text)
        print(d)
        print(len(d))
        print(len(a))
        print(len(h))
        driver.close()
        for j in range(len(h)):
            Count = Count+1
            call = call+1
            returnvalue = Scrape(a[j],h[j],text,d[j],sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                print('continue')
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    return

# def LazyLoading(MainURL,urlclass,heading,date,text,loadmore,footerclass,webname,webid):
    
#     sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
#     myid = 0
#     driver = driverget()
#     driver.get(MainURL)
#     time.sleep(2)
#     for i in range(30):
#         l = driver.find_element_by_class_name(footerclass)
#         driver.execute_script("arguments[0].scrollIntoView(true);", l)
#         try:
#             driver.find_elements_by_class_name(loadmore).click
#             time.sleep(2)
#         except:
#             print('continue')
#         time.sleep(3)

#     elems1 = driver.find_elements_by_class_name(urlclass)
#     a_tag = []
#     for k in elems1:
#         a_tag.append(k.find_element_by_tag_name('a'))
#         l=[]
#         for b in a_tag:
#             l.append(b.get_attribute('href'))
#     heading = driver.find_elements_by_class_name(heading)
#     heading_list = []
#     for i in heading:
#         heading_list.append(i.text)
#     date = driver.find_elements_by_class_name(date)
#     date_list = []
#     for i in date:
#         date_list.append(i.text)
#     driver.close()
#     for j in range(len(l)):
#         call = call + 1
#         Count = COunt + 1
#         returnvalue = Scrape(l[j],heading_list[j],text,date_list[j],sid,sname,Count,webname,current_aricle_heading,call)
#         if(returnvalue != 0):
#             continue
#         else:
#             break
#     return

def Main_Article_onsamepage(MainURL,start,end,operator,logic_number,heading,text,date,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    for i in range(start,end):
        if(operator == 'mul'):
            myid = i*logic_number
        if(operator == 'add'):
            myid = i+logic_number
        driver = driverget()
        driver.get(MainURL+str(myid))
        driver.maximize_window()
        time.sleep(1)
        h=[]
        a=[]
        try:
            driver.find_element_by_class_name('filter-by').click()
            time.sleep(5)
            btn_click = driver.find_element_by_xpath('/html/body/main/section[4]/div/div/div/div/button[2]')
            driver.execute_script("arguments[0].click();", btn_click);
            time.sleep(2)
        except:
            print('continue')
        Heading_list = driver.find_elements_by_class_name(heading)
        anchor_list = driver.find_elements_by_class_name('info')
        for i in Heading_list:
            h.append(i.text)
        for i in anchor_list:
            a_list = i.find_elements_by_tag_name('a')
            for c in a_list:
                a.append(c.get_attribute('href'))
        p = []
        Article_list = driver.find_elements_by_class_name(text)
        for i in Article_list:
            p.append(i.text)
        
        d = []
        print('except')
        for i in range(len(h)):
            d.append('date')
        print(len(d))
        print(len(h))
        print(len(a))
        print(len(p))
        driver.close()
        for j in range(len(h)):
            call = call + 1
            Count = Count+1
            print(h[j])
            print(current_article_heading)
            print(str(h[j]) == current_article_heading)
            if(str(h[j]) == current_article_heading):
                call = call - 1
                print('ifff')
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
            else:
                print('elseeee')
                if call == 1:
                    print('this is the latest article')
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                    # cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                    mydb.commit()
                    mydb.close()
                mydb = dbconnect()
                cursor = mydb.cursor()
                query1 = 'INSERT INTO ['+ webname +'](article_url,article_heading1,article_text,article_date_website,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?)'
                print(query1)
                val1 = (a[j],h[j],p[j],d[j],sid,sname,sid + 'A' + str(Count))
                cursor.execute(query1, val1)
                mydb.commit()
                mydb.close()
    return
def Main_Article_onsamepage1(MainURL,start,end,operator,logic_number,section,url,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    for i in range(start,end):
        if(operator == 'mul'):
            myid = i*logic_number
        if(operator == 'add'):
            myid = i+logic_number
        driver = driverget()
        driver.get(MainURL+str(myid))
        time.sleep(1)
        h=[]
        a=[]
        d= []
        p= []
        Heading_list = driver.find_elements_by_class_name(section)
        for i in Heading_list:
            ad = i.find_elements_by_tag_name('p')
            h.append(i.find_element_by_tag_name('h2').text)
            d.append(ad[0].text)
            p.append(ad[1].text)
            a.append(i.find_element_by_class_name(url).find_element_by_tag_name('a').get_attribute('href'))
        print(len(h))
        print(len(a))
        print(len(d))
        driver.close()
        for j in range(len(h)):
            call = call + 1
            Count = Count + 1
            # print(Heading)
            print(h[j])
            print(current_article_heading)
            print(str(h[j]) == current_article_heading)
            if(str(h[j]) == current_article_heading):
                call = call - 1
                print('ifff')
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
            else:
                print('elseeee')
                if call == 1:
                    print('this is the latest article')
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                    # cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                    mydb.commit()
                    mydb.close()
                mydb = dbconnect()
                cursor = mydb.cursor()
                query1 = 'INSERT INTO ['+ webname +'](article_url,article_heading1,article_text,article_date_website,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?)'
                print(query1)
                val1 = (a[j],h[j],p[j],d[j],sid,sname,sid + 'A' + str(Count))
                cursor.execute(query1, val1)
                mydb.commit()
                mydb.close()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
        mydb.commit()
        mydb.close()
        return
    return
def Google_Health_CaseStudy(MainURL,Mainclass,Footerclass,Linkclass,ulclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(3)
    href_links = []
    li = driver.find_element_by_class_name(ulclass).find_elements_by_tag_name('li')
    print(len(li))
    def inner(Mainclass,Footerclass):
        Links = driver.find_element_by_class_name(Mainclass).find_elements_by_class_name(Footerclass)
        for i in Links:
            if('Read case study' in (i.find_element_by_tag_name('a').get_attribute('track-name'))):
                href_links.append(i.find_element_by_tag_name('a').get_attribute('href'))
    inner(Mainclass,Footerclass)    
    for i in range(2,len(li)-1):
        li[i+1].click()
        inner(Mainclass,Footerclass)
    print(len(href_links))
    driver.close()
    Final =[]
    for j in href_links:
        driver = driverget()
        driver.get(j)
        time.sleep(3)
        Header = driver.find_element_by_tag_name('h1').text
        Text = driver.find_elements_by_tag_name('p')
        Text1 = []
        for p in Text:
            Text1.append(p.text)
        s = "."
        Text = s.join(Text1)
        Date = ''
        driver.close()
        # Result = {}
        # Result['Website'] = Website
        # Result['Heading'] = Header
        # Result['Text'] = Text
        # Result['Date'] = Date
        # Result['URL'] = j
        # Final.append(Result)

        call = call + 1
        Count = Count+1
        print(Header)
        print(current_article_heading)
        print(str(Header) == current_article_heading)
        if(str(Header) == current_article_heading):
            call = call - 1
            print('ifff')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
        else:
            print('elseeee')
        if call == 1:
            print('this is the latest article')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (Header, webname))
            # cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (Header, webname))
            mydb.commit()
            mydb.close()
        mydb = dbconnect()
        cursor = mydb.cursor()
        query1 = 'INSERT INTO ['+ webname +'](article_url,article_heading1,article_text,article_date_website,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?)'
        print(query1)
        val1 = (j,Header,Text,Date,sid,sname,sid + 'A' + str(Count))
        cursor.execute(query1, val1)
        mydb.commit()
        mydb.close()
    return

def Direct1(MainURL,heading,text,date,urlclass,webname,webid):
    
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    driver = driverget()
    driver.get(MainURL)
    time.sleep(3)
    call = 0
    elems1 = driver.find_element_by_class_name(urlclass).find_elements_by_tag_name('a')
    l=[]
    for b in elems1:
        l.append(b.get_attribute('href'))

    if(len(l) == 0):
        elems1 = driver.find_elements_by_class_name(urlclass)
        l=[]
        for b in elems1:
            l.append(b.get_attribute('href'))
    try:
        date_list = driver.find_element_by_class_name(date).find_elements_by_tag_name('li')
        d = []
        for i in date_list:
            d.append(i.text)
        driver.close()
        for j in range(len(l)):
            call = call + 1
            Count = Count + 1
            returnvalue = Scrape(l[j],heading,text,d[j],sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    except:
        driver.close()
        for i in l:
            call = call + 1
            Count = Count + 1
            returnvalue = Scrape(i,heading,text,date,sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    return


def LazyLoading(MainURL,urlclass,heading,date,text,footerclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(2)
    driver.maximize_window()
    for i in range(40):
        try:
            l = driver.find_element_by_class_name('load-more__button')
            driver.execute_script("arguments[0].scrollIntoView(true);", l)
        except:
            l = driver.find_element_by_class_name(footerclass)
            driver.execute_script("arguments[0].scrollIntoView(true);", l)
    # load-more__button 
        try:
            driver.find_element_by_class_name('load-more__button').click()
            time.sleep(2)
        except:
            print('continue')
        time.sleep(3)

    elems1 = driver.find_elements_by_class_name(urlclass)
    print(len(elems1))
    a_tag = []
    for k in elems1:
        a_tag.append(k.find_element_by_tag_name('a'))
        l=[]
        for b in a_tag:
            l.append(b.get_attribute('href'))
    heading = driver.find_elements_by_class_name(heading)
    heading_list = []
    for i in heading:
        heading_list.append(i.text)
    
    dateli = driver.find_elements_by_class_name(date)


    if(len(dateli)!=0):
        date_list = []
        for i in dateli:
            date_list.append(i.text)
        driver.close()

        for j in range(len(l)):
            call = call + 1
            Count = Count + 1
            returnvalue = Scrape(l[j],heading_list[j],text,date_list[j],sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return

    else:
        for j in range(len(l)):
            call = call + 1
            Count = Count + 1
            returnvalue = Scrape(l[j],heading_list[j],text,date,sid,sname,Count,webname,current_article_heading,call)
            if(returnvalue != 0):
                continue
            else:
                call = call - 1
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                mydb.commit()
                mydb.close()
                return
    return

def Ajax(MainURL,btnid,urlclass,heading,date,text,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    driver.maximize_window()
    time.sleep(2)
    def innerfunction():
        try:
            driver.find_element_by_class_name('gsight2_inviteDialog_neverButton').click()
        except:
            print('Continue')
        time.sleep(1)
        try:
            element = driver.find_element_by_class_name(btnid).find_element_by_tag_name('a').click()
        except:
            element = driver.find_element_by_id(btnid).click()
        try:
            driver.find_element_by_id(btnid)
            innerfunction()
        except:
            return
    innerfunction()

    elems1 = driver.find_elements_by_class_name(urlclass)
    print(len(elems1))
    heading = driver.find_elements_by_class_name(heading)
    date = driver.find_elements_by_class_name(date)
    driver.implicitly_wait(20)
    try:
        driver.find_element_by_class_name('gsight2_inviteDialog_neverButton').click()
    except:
        print('Continue')
    l = []
    for b in elems1:
        l.append(b.find_element_by_tag_name('a').get_attribute('href'))
    print(l)
    heading_list = []
    date_list = []
    for i in heading:
        heading_list.append(i.text)
    for i in date:
        date_list.append(i.text) 
    driver.close()
    for j in range(len(l)):
        Count = Count + 1
        call = call + 1
        returnvalue = Scrape(l[j],heading_list[j],text,date_list[j],sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
    return

def Ajax2(MainURL,btnid,urlclass,date,text,footerclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(4)
    driver.maximize_window()
    time.sleep(2)
    l = driver.find_element_by_class_name(footerclass)
    driver.execute_script("arguments[0].scrollIntoView(true);", l)

    def innerfunction():
        time.sleep(1)
        try:
            element = driver.find_element_by_class_name(btnid).find_element_by_tag_name('a').click()
        except:
            element = driver.find_element_by_id(btnid).click()
        time.sleep(2)
        l = driver.find_element_by_class_name(footerclass)
        driver.execute_script("arguments[0].scrollIntoView(true);", l)
        time.sleep(4)
        try:
            driver.find_element_by_class_name(btnid).find_element_by_tag_name('a')
            innerfunction()
        except:
            return
    innerfunction()
    date = driver.find_elements_by_class_name(date)
    heading = driver.find_elements_by_class_name(urlclass)
    try:
        driver.find_element_by_class_name('gsight2_inviteDialog_neverButton').click()
    except:
        print('Continue')
    print(len(date))
    print(len(heading))
    l = []
    for b in heading:
        l.append(b.find_element_by_tag_name('a').get_attribute('href'))
    heading_list = []
    date_list = []
    a_list = []
    for i in heading:
        heading_list.append(i.text)
    for i in date:
        date_list.append(i.text)
    driver.close()
    for j in range(len(l)):
        Count = Count + 1
        call = call + 1
        returnvalue = Scrape(l[j],heading_list[j],text,date_list[j],sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
    return

def Ajax3(MainURL,btnid,urlclass,heading,date,text,footerclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(4)
    driver.maximize_window()
    time.sleep(2)
    def innerfunction():
        time.sleep(1)
        try:
            element = driver.find_element_by_class_name(btnid).find_element_by_tag_name('a').click()
        except:
            element = driver.find_element_by_id(btnid).click()
        time.sleep(4)
        from selenium.webdriver.common.action_chains import ActionChains
        element = driver.find_element_by_id(btnid)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        try:
            driver.find_element_by_id(btnid)
            innerfunction()
        except:
            print('not found')
            return
    innerfunction()
    
    elems1 = driver.find_element_by_id(urlclass).find_elements_by_tag_name('a')
    del elems1[4]
    heading = driver.find_element_by_id(urlclass).find_elements_by_class_name(heading)
    # date = driver.find_element_by_id(urlclass).find_elements_by_class_name(date)
    print(len(elems1))
    # print(len(date))
    print(len(heading))
    l = []
    for b in elems1:
        l.append(b.get_attribute('href'))
    heading_list = []
    date_list = []
    for i in heading:
        heading_list.append(i.text)
    # for i in date:
    #     date_list.append(i.text)
    for j in range(len(l)):
        Count = Count + 1
        call = call + 1
        returnvalue = Scrape(l[j],heading_list[j],text,date,sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
    return

def Ajax4(MainURL,btnid,heading,footerclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(4)
    driver.maximize_window()
    time.sleep(2)
    fo = driver.find_element_by_class_name(footerclass)
    driver.execute_script("arguments[0].scrollIntoView(true);", fo)
    def innerfunction():
        time.sleep(1)
        try:
            print('try')
            element = driver.find_element_by_class_name('pager__item').find_element_by_class_name(btnid).click()
        except:
            print('except')
            element = driver.find_element_by_id(btnid).click()
        time.sleep(4)
        from selenium.webdriver.common.action_chains import ActionChains
        element = driver.find_element_by_class_name(btnid)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        try:
            driver.find_element_by_class_name(btnid)
            innerfunction()
        except:
            print('not found')
            return
    innerfunction()
    
    heading_list = []
    date_list = []
    a_tag = []
    l=[]
    try:
        heading = driver.find_elements_by_class_name(heading)
        for i in heading:
            heading_list.append(i.text)
            a_tag.append(i.find_element_by_tag_name('a'))
            for b in a_tag:
                l.append(b.get_attribute('href'))
    except:
        heading = ''
        heading_list.append(heading)
    try:
        date = driver.find_elements_by_class_name(date)
        for i in date:
            date_list.append(i.text)
    except:
        date = ''
        date_list.append(date)

    driver.close()
    for j in range(len(heading_list)):
        call = call + 1
        Count = Count+1
        # print(Heading)
        print(h[j])
        print(current_article_heading)
        print(str(h[j]) == current_article_heading)
        if(str(h[j]) == current_article_heading):
            print('ifff')
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
        else:
            print('elseeee')
            if call == 1:
                print('this is the latest article')
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                # cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (h[j], webname))
                mydb.commit()
                mydb.close()
            mydb = dbconnect()
            cursor = mydb.cursor()
            query1 = 'INSERT INTO ['+ webname +'](article_url,article_heading1,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?)'
            print(query1)
            val1 = (l[j],heading_list[j],sid,sname,sid + 'A' + str(Count))
            cursor.execute(query1, val1)
            mydb.commit()
            mydb.close()
        return
    return


def Direct2(MainURL,heading,text,date,urlclass,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    driver = driverget()
    driver.get(MainURL)
    time.sleep(3)
    elems1 = driver.find_element_by_class_name(urlclass).find_elements_by_tag_name('a')
    l=[]
    for b in elems1:
        l.append(b.get_attribute('href'))
    
    h=[]
    heading_list = driver.find_element_by_class_name(heading).find_elements_by_tag_name('a')
    for i in heading_list:
        h.append(i.text)
    date_list = driver.find_elements_by_class_name(date)
    d = []
    for i in date_list:
        d.append(i.text)
    print(len(l))
    print(len(d))
    print(len(h))
    driver.close()
    for j in range(len(l)):
        Count = Count + 1
        call = call + 1
        returnvalue = Scrape(l[j],h[j],text,d[j],sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return
            
    return

def Doublepagination(MainURL,start,end,operator,logic_number,urlclass,heading,text,date,webname,webid):
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    for i in range(start,end,logic_number):
        driver = driverget()
        driver.get(MainURL+str(i))
        for j in range(1,6):
            driver.get(MainURL+str(myid)+'?page='+str(j))
            time.sleep(3)
            try:
                elems1 = driver.find_elements_by_class_name(urlclass)
                a_tag = []
                headings = []
                for k in elems1:
                    a_tag.append(k.find_element_by_tag_name('a'))
                    l=[]
                    for b in a_tag:
                        l.append(b.get_attribute('href'))
                for h in elems1:
                    headings.append(h.find_element_by_tag_name('a').text)
            except:
                print('not found')
            driver.close()
            for a in range(len(l)):
                call = call + 1 
                Count = Count + 1
                returnvalue = Scrape(l[a],headings[a],text,date,sid,sname,Count,webname,current_article_heading,call)
                if(returnvalue != 0):
                    continue
                else:
                    call = call - 1
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
                    mydb.commit()
                    mydb.close()
                    return
    return
def Ajax_pagination(MainURL,urlclass,heading,date,text,ulclass,liclass,webname,webid):
    def inner(MainURL,urlclass,heading,date,text,ulclass,liclass,sid,sname,current_article_heading,Count,call):
        time.sleep(4)
        li=[]
        li = driver.find_element_by_class_name(ulclass).find_elements_by_tag_name('li')
        print(len(li))
        for a in range(len(li)-1,0,-1):
            # print(driver.find_element_by_class_name('pagination').find_element_by_class_name('active').text)
            if(li[a].get_attribute("class") == liclass ):
                # try:
                elems1 = driver.find_elements_by_class_name(urlclass)
                try:
                    dates = driver.find_elements_by_class_name(date)
                except Exception as e:
                    print(e)
                a_tag = []
                for k in elems1[::-1]:
                    a_tag.append(k.find_element_by_tag_name('a'))
                    for b in a_tag:
                        l.append(b.get_attribute('href'))
                for i in elems1[::-1]:
                    heading_list.append(i.text)
                for i in dates[::-1]:
                    date_list.append(i.text)
                if(li[a-1].get_attribute('class') == 'disabled'):
                    print('first page')
                    return
                else:
                    li[a-1].find_element_by_tag_name('a').click()
                    time.sleep(4)
                    inner(MainURL,urlclass,heading,date,text,ulclass,liclass,sid,sname,current_article_heading,Count,call)
                    return
    driver = driverget()
    driver.get(MainURL)
    heading_list = []
    date_list = []
    l=[]
    time.sleep(3)
    last = driver.find_element_by_class_name(ulclass).find_elements_by_tag_name('li')
    print(len(last))
    for i in range(len(last)):
        try:
            if(last[i].find_element_by_tag_name('a').get_attribute("aria-label") == 'Next'):
                print('found')
                last[i].find_element_by_tag_name('a').click()
            else:
                print('not found')
        except:
            print('continue')
    sid,sname,current_article_heading,Count = Neededinputs(webid,webname)
    call = 0
    inner(MainURL,urlclass,heading,date,text,ulclass,liclass,sid,sname,current_article_heading,Count,call)
    for j in range(len(l)):
        Count = Count + 1
        call = call + 1
        returnvalue = Scrape(l[j],heading_list[j],text,date_list[j],sid,sname,Count,webname,current_article_heading,call)
        if(returnvalue != 0):
            continue
        else:
            call = call - 1
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set new_articles=? where section_name=?""", (call, webname))
            mydb.commit()
            mydb.close()
            return





#Step – 2 (configuring your application)
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'

#step – 3 (creating a dictionary to store information about users)



# user = [{"username": "approver", "password": "damo2021","usertype":"Approver"},{"username": "analyst1", "password": "damo2021","usertype":"Analyst"},{"username": "admin1", "password": "damo2021","usertype":"Admin"},{"username": "superadmin", "password": "damo2021","usertype":"Superadmin"}]

# Step – 4 (creating route for login)

    # print(data1)
@app.route('/', methods = ['POST', 'GET'])
def index():
    return redirect('/login')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('uname')
        password = request.form.get('pwd')
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        exist_query = cursor3.execute("""SELECT username,password FROM users where username =? and password=?""",(username,password))
        account = cursor3.fetchone()
        print(account)
        mydb.close()
        if account:
            session['user'] = account[0]
            session['pwd'] = account[1]
            # refresh_status =  'incomplete'
            if 'user' in session:
                mydb = dbconnect()
                cursor = mydb.cursor()
                role = cursor.execute("""SELECT (role) FROM users where username =? and password=?""",(session['user'],session['pwd']))
                user_role = cursor.fetchone()
                session['usertype'] = user_role[0]
                print('hello')
                return redirect('/dashboard')
            else:
                return redirect('/login')
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html',msg = msg)
    return render_template("login.html",variable="Incorrect password or User doesn't exist")

#Step -5(creating route for dashboard and logout)
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        mydb = dbconnect()
        logintime = datetime.now()
        logintime = logintime.replace(microsecond=0)
        cursor1 = mydb.cursor()
        cursor1.execute("""update users set last_loggedin=? where username=?""", (logintime, session['user']))
        mydb.commit()
        mydb.close()
        mydb = dbconnect()
        cursor2 = mydb.cursor()
        cursor2.execute("select * from schema_mapping_data")
        data1 = cursor2.fetchall()
        return render_template("Scraper.php",variable={'username': session['user'],'usertype': session['usertype'],'data':data1})
    else:
        return redirect('/login')


@app.route('/Scraper')
def Scraper():
    if 'user' in session:
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        cursor3.execute("select * from schema_mapping_data")
        data1 = cursor3.fetchall()
        # print(type(data1))
        if(session['usertype'] == 'Admin' or session['usertype'] == 'Analyst' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Approver'):
            return render_template('Scraper.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1})
        else:
            return render_template('login.html')
    else:
        return redirect('/login')

@app.route('/View')
def View():
    if 'user' in session:
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        cursor3.execute("select * from schema_mapping_data")
        data1 = cursor3.fetchall()
        if(session['usertype'] == 'Analyst' or session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Admin' ):
            return render_template('View.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1})
        else:
            return render_template('login.html')
    else:
        return redirect('/login')


@app.route('/Production_tab')
def Production_tab():
    if 'user' in session:
        pagefirstid = request.args.get('pgno')
        filevalid = request.args.get('valid')
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        cursor3.execute("select * from production_table order by id desc OFFSET "+ str(pagefirstid) +" ROWS FETCH NEXT 10 ROWS ONLY")
        data1 = cursor3.fetchall()
        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Admin' ):
            return render_template('production.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1,'pgid':pagefirstid,'valid':filevalid})
        else:
            return render_template('login.html')
    else:
        return redirect('/login')


@app.route('/Notification_tab')
def Notification_tab():
    if 'user' in session:
        pagefirstid = request.args.get('pgno')
        filevalid = request.args.get('valid')
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        cursor3.execute("select * from Notification order by id desc OFFSET "+ str(pagefirstid) +" ROWS FETCH NEXT 10 ROWS ONLY")
        data1 = cursor3.fetchall()
        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Admin' ):
            return render_template('notifications.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1,'pgid':pagefirstid,'valid':filevalid})
        else:
            return render_template('login.html')
    else:
        return redirect('/login')



@app.route('/Display')
def Display():
    if 'user' in session:
        value = request.args.get('id')
        pagefirstid = request.args.get('pgno')
        filevalid = request.args.get('valid')
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        print(value)
        d = cursor1.execute("select * from [" +value+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '') order by id OFFSET "+ str(pagefirstid) +" ROWS FETCH NEXT 10 ROWS ONLY")
        print(d)
        data = cursor1.fetchall()
        mydb.close()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        articlecount = cursor1.execute("Select count(*) from ["+value+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '')")
        articlecount = cursor1.fetchone()
        articlecount = articlecount[0]
        print('A count is '+str(articlecount))
        pages = math.ceil(int(articlecount) / 10)
        if(session['usertype'] == 'Analyst'):
            return render_template('dashboard1.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value,'valid':filevalid,'articlecount':articlecount,'noofpages':pages})
        elif(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
            return render_template('dashboard2.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value,'valid':filevalid,'articlecount':articlecount,'noofpages':pages})
        elif( session['usertype'] == 'Admin'):
            return render_template('dashboard.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value,'valid':filevalid,'articlecount':articlecount,'noofpages':pages})
    else:
        return redirect('/login')

@app.route('/users_page')
def users_page():
    if 'user' in session:
        if(session['usertype'] == 'Admin' or session['usertype'] == 'Superadmin' ):
            mydb = dbconnect()
            cursor4 = mydb.cursor()
            cursor4.execute("select * from users")
            data = cursor4.fetchall()
            mydb.close()
            return render_template('users.php',variable={'username': session['user'],'usertype': session['usertype'] ,'data':data})
        else:
            return render_template('login.html')
    else:
        return redirect('/login')

@app.route('/delete_user',methods = ['POST', 'GET'])
def delete_user():
    if(request.method == 'POST'):
        value = request.get_json()
        print(value['data'])
        mydb = dbconnect()
        logintime = datetime.now()
        cursor1 = mydb.cursor()
        cursor1.execute("""delete from users where ID=?""", (value['data']))
        mydb.commit()
        mydb.close()
        return  {'success':True}
        # return render_template('users.php',variable={'username': session['user'],'usertype': session['usertype'] ,'data':data})

@app.route('/edit_row',methods = ['POST','GET'])
def edit_row():
    if(request.method == 'POST'):
        value = request.get_json()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        print(value['data'])
        cursor1.execute("select article_id from [" +value['data1']+"] where article_id = ?",value['data'])
        aid = cursor1.fetchone()
        article_id = aid.article_id
        cursor1.execute("select article_heading1 from [" +value['data1']+"] where article_id = ?",value['data'])
        ah = cursor1.fetchone()
        article_heading = ah.article_heading1
        cursor1.execute("select article_text from [" +value['data1']+"] where article_id = ?",value['data'])
        at = cursor1.fetchone()
        article_text = at.article_text
        cursor1.execute("select article_date_website from [" +value['data1']+"] where article_id = ?",value['data'])
        ad = cursor1.fetchone()
        article_date_website = ad.article_date_website
        cursor1.execute("select Technology_keyword from [" +value['data1']+"] where article_id = ?",value['data'])
        ate = cursor1.fetchone()
        Technology = ate.Technology_keyword
        cursor1.execute("select Use_Case_Keyword from [" +value['data1']+"] where article_id = ?",value['data'])
        ab = cursor1.fetchone()
        broad_use_case = ab.Use_Case_Keyword
        cursor1.execute("select Healthcare_Enterprise_Keyword from [" +value['data1']+"] where article_id = ?",value['data'])
        ahs = cursor1.fetchone()
        health_system = ahs.Healthcare_Enterprise_Keyword
        cursor1.execute("select vendor_keyword from [" +value['data1']+"] where article_id = ?",value['data'])
        av = cursor1.fetchone()
        vendor = av.vendor_keyword
        cursor1.execute("select vendor_product from [" +value['data1']+"] where article_id = ?",value['data'])
        avd = cursor1.fetchone()
        vendor_product = avd.vendor_product
        cursor1.execute("select speciality from [" +value['data1']+"] where article_id = ?",value['data'])
        asp = cursor1.fetchone()
        speciality = asp.speciality
        cursor1.execute("select article_url from [" +value['data1']+"] where article_id = ?",value['data'])
        au = cursor1.fetchone()
        article_url = au.article_url
        cursor1.execute("select section_type from [" +value['data1']+"] where article_id = ?",value['data'])
        ast = cursor1.fetchone()
        section_type = ast.section_type
        mydb.close()
        # return {'data':data}
        return {'sucess':[article_heading,article_text,article_date_website,Technology,broad_use_case,health_system,vendor,vendor_product,speciality,article_url,value['data'],section_type]}

@app.route('/Savechanges',methods = ['POST','GET'])
def Savechanges():
    if(request.method == 'POST'):
        articleid = request.form.get('aid')
        articledate = request.form.get('date')
        articleheading = request.form.get('heading')
        articletext = request.form.get('text')
        articlekeywords = request.form.get('keywords')
        Technology = request.form.get('Technology')
        health_system = request.form.get('health_system')
        broad_use_case = request.form.get('broad_use_case')
        vendor = request.form.get('vendor')
        vendor_product = request.form.get('vendor_product')
        speciality = request.form.get('speciality')
        article_url = request.form.get('article_url')
        webname = request.form.get('webname')
        pgid1 = request.form.get('pgid1')
        section_type = request.form.get('section_type')
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update ["""+ webname +"""]  set article_heading1=?,article_text=?,article_date_website=?,Technology_keyword=?,Use_Case_Keyword=?,Healthcare_Enterprise_Keyword=?,vendor_keyword=?,vendor_product=?,speciality=?,article_url=? where article_id=?""", (articleheading,articletext,articledate,Technology,broad_use_case,health_system,vendor,vendor_product,speciality,article_url,articleid))
        mydb.commit()
        fileupload = ''
        if(session['usertype'] == 'Analyst'):
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Updates' where article_id = ?""",articleid)
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",articleid)
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],articleid))
            mydb.commit()
            mydb.close()
    return redirect('/Display?id='+webname+'&pgno='+str(pgid1)+'&valid='+fileupload)

@app.route('/Savechanges_notify',methods = ['POST','GET'])
def Savechanges_notify():
    if(request.method == 'POST'):
        articleid = request.form.get('aid')
        articledate = request.form.get('date')
        articleheading = request.form.get('heading')
        articletext = request.form.get('text')
        articlekeywords = request.form.get('keywords')
        Technology = request.form.get('Technology')
        health_system = request.form.get('health_system')
        broad_use_case = request.form.get('broad_use_case')
        vendor = request.form.get('vendor')
        vendor_product = request.form.get('vendor_product')
        speciality = request.form.get('speciality')
        article_url = request.form.get('article_url')
        webname = request.form.get('webname')
        pgid1 = request.form.get('pgid1')
        section_type = request.form.get('section_type')
        print(articledate)
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update ["""+ webname +"""]  set article_heading1=?,article_text=?,keywords_mapped=?,article_date_website=?,Technology_Keyword=?,Use_Case_Keyword=?,Healthcare_Enterprise_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_url=? where article_id=?""", (articleheading,articletext,articlekeywords,articledate,Technology,broad_use_case,health_system,vendor,vendor_product,speciality,article_url,articleid))
        mydb.commit()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("Update ["+webname+"] set approval_status = 'Update by Approver' where article_id = ?",articleid)
        mydb.commit()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("Update Notification set approval_status = 'Update by Approver' where article_id = ?",articleid)
        mydb.commit()
        mydb.close()
        return redirect('/Notification_tab?pgno='+pgid1)

@app.route('/Savechanges_production',methods = ['POST','GET'])
def Savechanges_production():
    if(request.method == 'POST'):
        articleid = request.form.get('aid')
        articledate = request.form.get('date')
        articleheading = request.form.get('heading')
        articletext = request.form.get('text')
        articlekeywords = request.form.get('keywords')
        Technology = request.form.get('Technology')
        health_system = request.form.get('health_system')
        broad_use_case = request.form.get('broad_use_case')
        vendor = request.form.get('vendor')
        vendor_product = request.form.get('vendor_product')
        speciality = request.form.get('speciality')
        article_url = request.form.get('article_url')
        webname = request.form.get('webname')
        pgid1 = request.form.get('pgid1')
        print('article date is ' +  articledate)
        print('artice id is ' + articleid)
        print(webname)
        print(broad_use_case)
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update ["""+ webname +"""]  set article_heading1=?,article_text=?,keywords_mapped=?,article_date_website=?,Technology_Keyword=?,Use_Case_Keyword=?,Healthcare_Enterprise_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_url=? where article_id=?""", (articleheading,articletext,articlekeywords,articledate,Technology,broad_use_case,health_system,vendor,vendor_product,speciality,article_url,articleid))
        # print("""update ["""+ webname +"""]  set article_heading1=?,article_text=?,keywords_mapped=?,article_date_website=?,Technology=?,broad_use_case=?,health_system=?,vendor=?,vendor_product=?,speciality=?,article_url=? where article_id=?""", (articleheading,articletext,articlekeywords,articledate,Technology,broad_use_case,health_system,vendor,vendor_product,speciality,article_url,articleid))
        mydb.commit()
        fileupload = ''
    return redirect('/Production_tab?pgno='+pgid1)

        


@app.route('/user_insert', methods = ['POST', 'GET'])
def user_insert():
    if(request.method == 'POST'):
        mydb = dbconnect()
        # uid = request.form.get('uid')
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        role = request.form.get('role')
        uid = str(uname[0:2]) +'_' +str(role[0:2])
        print(uid)
        cursor5 = mydb.cursor()
        created_date = date.today()
        query1 = 'INSERT INTO users(userid,username,password,role,Date_created,createdby,last_loggedin) VALUES (?,?,?,?,?,?,?)'
        val1 = (uid,uname,pwd,role,created_date,session['user'],'not yet loggedin')
        cursor5.execute(query1, val1)
        mydb.commit()
        mydb.close()
        mydb = dbconnect()
        cursor6 = mydb.cursor()
        cursor6.execute("select * from users")
        data = cursor6.fetchall()
        mydb.close()
        return render_template('users.php',variable={'username': session['user'],'usertype': session['usertype'] ,'data':data})

# @app.route('/Edit1')
# def Edit1():
    
    
@app.route('/Password')
def Password():
    return render_template('Change.html')


@app.route('/ChangePassword',methods = ['POST', 'GET'])
def ChangePassword():
    return render_template('changepwd.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd']})

@app.route('/forgot_pwd',methods = ['POST', 'GET'])
def forgot_pwd():
    if(request.method == 'POST'):
        old_password = request.form.get('Old_Password')
        new_password = request.form.get('New_Password')
        confirm_password = request.form.get('Confirm_Password')
        print(old_password)
        print(new_password)
        print(confirm_password)
        mydb = dbconnect()
        if( old_password == session['pwd'] and new_password == confirm_password):
            cursor1 = mydb.cursor()
            cursor1.execute("""update users set password=? where username=?""", (new_password,session['user']))
            mydb.commit()
            mydb.close()
            return render_template('changepwd.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd'],'msg':'Password changed successfully !! '})
        elif(old_password != session['pwd']):
            print('here')
            return render_template('changepwd.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd'],'msg':'Incorrect old password '})
        elif(new_password != confirm_password):
            return render_template('changepwd.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd'],'msg':"New password and Confirm password doesn't match "})

        

# Step -6(creating route for logging out)
@app.route('/logout')
def logout():
    session.pop('user')     
    return redirect('/login')

@app.route('/Scrapeit',methods = ['POST', 'GET'])
def Scrapeit():
    TEMP=0
    if(request.method == 'POST'):
        value = request.get_json()
        print(value['data'])
        # value = request.args.get('website-name')
        status = []
        for i in value['data']:
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select refresh_status from schema_mapping_data where section_name=?",(i))
            v1 = cursor1.fetchone()
            refstatus = v1.refresh_status
            if( refstatus != 'In progress'):
                print('Started scraping')
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set refresh_status='In progress' where section_name=?""",i)
                mydb.commit()
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select parameters from function_with_parameters where website_name=?",(i))
                v1 = cursor1.fetchone()
                param = v1.parameters
                cursor1.execute("select function_name from function_with_parameters where website_name=?",(i))
                v2 = cursor1.fetchone()
                fname = v2.function_name
                cursor1.execute("select website_name from function_with_parameters where website_name=?",(i))
                v3 = cursor1.fetchone()
                wbname = v3.website_name
                cursor1.execute("select website_id from function_with_parameters where website_name=?",(i))
                v4 = cursor1.fetchone()
                wbid = v4.website_id
                mydb.close()
                param_list = param.split(",")
                print(param_list)
                print(fname)
                print(wbname)
                print(wbid)
                if(fname == 'Main'):
                    t1 = Thread(target=Main, args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                    t1.start()
                    t1.join()

                elif(fname == 'Direct'):
                    t2 = Thread(target=Direct, args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                    t2.start()
                    t2.join()

                elif(fname == 'Main_General'):
                    t3 = Thread(target=Main_General, args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],param_list[10],wbname,wbid))
                    t3.start()
                    t3.join()

                elif(fname == 'Main2'):
                    t4 = Thread(target=Main2,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                    t4.start()
                    t4.join()
                elif(fname == 'LazyLoading'):
                    t5 = Thread(target=LazyLoading,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                    t5.start()
                    t5.join()

                elif(fname == 'Main_Article_onsamepage'):
                    t6 = Thread(target=Main_Article_onsamepage,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],wbname,wbid))
                    t6.start()
                    t6.join()
                elif(fname == 'Main_Article_onsamepage1'):
                    t7 = Thread(target=Main_Article_onsamepage1,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],wbname,wbid))
                    t7.start()
                    t7.join()
                elif(fname == 'Google_Health_CaseStudy'):
                    t8 = Thread(target=Google_Health_CaseStudy,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                    t8.start()
                    t8.join()
                elif(fname == 'Direct1'):
                    t9 = Thread(target=Direct1,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                    t9.start()
                    t9.join()
                elif(fname == 'Direct2'):
                    t10 = Thread(target=Direct2,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                    t10.start()
                    t10.join()
                elif(fname == 'Doublepagination'):
                    t11 = Thread(target=Doublepagination,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                    t11.start()
                    t11.join()

                elif(fname == 'Ajax'):
                    t12 = Thread(target=Ajax,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                    t12.start()
                    t12.join()

                elif(fname == 'Ajax2'):
                    t13 = Thread(target=Ajax2,args=(param_list[1],param_list[2],param_list[3],param_list[5],param_list[6],param_list[7],wbname,wbid))
                    t13.start()
                    t13.join()
                elif(fname == 'Ajax3'):
                    t14 = Thread(target=Ajax3,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],param_list[7],wbname,wbid))
                    t14.start()
                    t14.join()
                elif(fname == 'Ajax4'):
                    t15 = Thread(target=Ajax4,args=(param_list[1],param_list[2],param_list[3],param_list[4],wbname,wbid))
                    t15.start()
                    t15.join()
                elif(fname == 'Ajax_pagination'):
                    t16 = Thread(target=Ajax_pagination,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],param_list[7],wbname,wbid))
                    t16.start()
                    t16.join()
                else:
                    print('Continue') 


                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set refresh_status='Completed' where section_name=?""",i)
                mydb.commit()
                lastrefresh = datetime.now()
                lastrefresh = lastrefresh.replace(microsecond=0)
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set last_refreshed_on=? where section_name=?""",(lastrefresh,i))
                mydb.commit()
                mydb.close()
                   
            # else:
            #     print('Continue')  
    return {'status':'success'}

@app.route('/Scrapeit_Single',methods = ['POST', 'GET'])
def Scrapeit_Single():
    if(request.method == 'POST'):
        value = request.get_json()
        value = (value['data'])
        print('table is' + value)
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("select refresh_status from schema_mapping_data where section_name=?",(value))
        # print("select refresh_status from schema_mapping_data where section_name=?",(value))
        v1 = cursor1.fetchone()
        refstatus = v1.refresh_status
        if(refstatus != 'In progress'):
            print('Started scraping')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set refresh_status='In progress' where section_name=?""",value)
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select parameters from function_with_parameters where website_name=?",(value))
            v1 = cursor1.fetchone()
            param = v1.parameters
            cursor1.execute("select function_name from function_with_parameters where website_name=?",(value))
            v2 = cursor1.fetchone()
            fname = v2.function_name
            cursor1.execute("select website_name from function_with_parameters where website_name=?",(value))
            v3 = cursor1.fetchone()
            wbname = v3.website_name
            cursor1.execute("select website_id from function_with_parameters where website_name=?",(value))
            v4 = cursor1.fetchone()
            wbid = v4.website_id
            mydb.close()
            param_list = param.split(",")
            print(param_list)
            print(fname)
            print(wbname)
            print(wbid)
            if(fname == 'Main'):
                st1 = Thread(target=Main, args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                #Main(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid,call)
                st1.start()
                st1.join()

            elif(fname == 'Direct'):
                st2 = Thread(target=Direct, args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                st2.start()
                st2.join()

            elif(fname == 'Main_General'):
                st3 = Thread(target=Main_General, args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],param_list[10],wbname,wbid))
                st3.start()
                st3.join()
            elif(fname == 'Main2'):
                st4 = Thread(target=Main2,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                st4.start()
                st4.join()
            elif(fname == 'LazyLoading'):
                st5 = Thread(target=LazyLoading,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                st5.start()
                st5.join()

            elif(fname == 'Main_Article_onsamepage'):
                st6 = Thread(target=Main_Article_onsamepage,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],wbname,wbid))
                st6.start()
                st6.join()
            elif(fname == 'Main_Article_onsamepage1'):
                st7 = Thread(target=Main_Article_onsamepage1,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],wbname,wbid))
                st7.start()
                st7.join()
            elif(fname == 'Google_Health_CaseStudy'):
                st8 = Thread(target=Google_Health_CaseStudy,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                st8.start()
                st8.join()
            elif(fname == 'Direct1'):
                st9 = Thread(target=Direct1,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                st9.start()
                st9.join()
            elif(fname == 'Direct2'):
                st10 = Thread(target=Direct2,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],wbname,wbid))
                st10.start()
                st10.join()
            elif(fname == 'Doublepagination'):
                st11 = Thread(target=Doublepagination,args=(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid))
                st11.start()
                st11.join()

            elif(fname == 'Ajax'):
                st12 = Thread(target=Ajax,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],wbname,wbid))
                st12.start()
                st12.join()

            elif(fname == 'Ajax2'):
                st13 = Thread(target=Ajax2,args=(param_list[1],param_list[2],param_list[3],param_list[5],param_list[6],param_list[7],wbname,wbid))
                st13.start()
                st13.join()
            elif(fname == 'Ajax3'):
                st14 = Thread(target=Ajax3,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],param_list[7],wbname,wbid))
                st14.start()
                st14.join()
            elif(fname == 'Ajax4'):
                st15 = Thread(target=Ajax4,args=(param_list[1],param_list[2],param_list[3],param_list[4],wbname,wbid))
                st15.start()
                st15.join()
            elif(fname == 'Ajax_pagination'):
                st16 = Thread(target=Ajax_pagination,args=(param_list[1],param_list[2],param_list[3],param_list[4],param_list[5],param_list[6],param_list[7],wbname,wbid))
                st16.start()
                st16.join()
            else:
                print('Continue') 
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set refresh_status='Completed' where section_name=?""",value)
            mydb.commit()
            lastrefresh = datetime.now()
            lastrefresh = lastrefresh.replace(microsecond=0)
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set last_refreshed_on=? where section_name=?""",(lastrefresh,value))
            mydb.commit()
            mydb.close() 
    return {'status':'success'}

@app.route('/Multirefreshstep1',methods = ['POST', 'GET'])
def Multirefreshstep1():
    if(request.method == 'POST'):
        val = request.get_json()
        print(val['data'])
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("Select count(id) from schema_mapping_data where refresh_status = 'In progress'") 
        activestatus = cursor1.fetchone()
        activestatus = activestatus[0]
        print('activestatus is '+ str(activestatus) )
        if(activestatus == 0):
            if(type(val['data']) == list):
                for i in val['data']:
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update schema_mapping_data set refresh_status='In Queue' where section_name=?""",i)
                    mydb.commit()
                    mydb.close()
                return {'flag':'canscrape','values':val['data']}
            else:
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set refresh_status='In Queue' where section_name=?""",val['data'])
                mydb.commit()
                mydb.close()
                return {'flag':'canscrape','values':val['data']}
        else:
            return {'flag':'cantscrape','values':activestatus}


@app.route('/Status',methods = ['POST', 'GET'])
def Status():
    if(request.method == 'POST'):
        val = request.get_json()
        final_status = []
        print(val['data'])
        final_dict = {}
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        if(type(val['data']) == list):
            for i in val['data']:
                mydict = {}
                cursor1.execute("select refresh_status from schema_mapping_data where section_name=? ",i)
                Value1 = cursor1.fetchone()
                stat = Value1.refresh_status
                mydict[i] = stat
                final_status.append(mydict)
            final_dict['status'] = final_status
            return final_dict
        else:
            final_dict = {}
            cursor1.execute("select refresh_status from schema_mapping_data where section_name=? ",val['data'])
            Value1 = cursor1.fetchone()
            stat = Value1.refresh_status
            final_dict['status'] = stat
            return jsonify(final_dict)
@app.route('/fileupload',methods = ['POST','GET'])
def fileupload():
    if(request.method == 'POST'):
        webname = request.form.get('webname')
        pgid = request.form.get('pgid')
        f = request.files['file']
        inputdf = pd.read_excel(f)
        inputdf.fillna('', inplace=True)
        shape = inputdf.shape
        headings_raw = ['Unnamed: 0', 'Article ID', 'Article Date', 'Healthcare Enterprise', 'Technology', 'Use Case', 'Vendor', 'Vendor Product', 'Speciality', 'Details', 'Article URL', 'Section Type', 'Approval Status', 'Rank', 'Vendor Count', 'Action: (U / A / D)']
        headings_dyn = list(inputdf.columns.values)
        print(headings_raw)
        print(headings_dyn)
        print(len(headings_raw))
        print(len(headings_dyn))
        flag = 0
        print(headings_raw==headings_dyn)
        if(headings_raw==headings_dyn):
            print('yes')
            for i,j in inputdf.iterrows():
                if(str(j[11]) == webname):
                    flag = 1
                    if(j[15] == 'U'):
                        print('update')
                        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update ["""+webname+"""] set article_date_website=?,Healthcare_Enterprise_Keyword=?,Technology_keyword=?,Use_Case_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_text=?,article_url=? where article_id=?""", (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[1])))
                            mydb.commit()
                        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
                            print('Insert into production')
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""INSERT INTO production_table (article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count) SELECT article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",str(j[1]))
                            mydb.commit()
                            mydb.close()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("Update ["+webname+"] set approval_status = 'Move to Production' where article_id = ?",str(j[1]))
                            mydb.commit()
                            mydb.close()
                        if(session['usertype'] == 'Admin' or session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("Update ["+webname+"] set approval_status = 'Sent for Approval' where article_id = ?",str(j[1]))
                            mydb.commit()
                            mydb.close()
                    elif(j[15] == 'D'):
                        print('delete')
                        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute('delete from ['+webname+'] where article_id=?',j[1])
                            mydb.commit()
                            mydb.close()
                    elif(j[15] == 'A'):
                        print('add')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("select section_id from schema_mapping_data where section_name =? ",webname)
                        Value1 = cursor1.fetchone()
                        sid = Value1.section_id
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("select id from [" +webname+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                        webid_point = cursor1.fetchone()
                        current_aricle_id = webid_point[0]
                        Count = int(current_aricle_id)
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = 'INSERT INTO ['+ webname +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),sid,webname,sid + 'A' + str(Count+1))
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
                            print('Insert into production')
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute('select article_id from ['+webname+'] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY')
                            article_id_var = cursor1.fetchone()
                            current_aricle_id = article_id_var[0]
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""INSERT INTO production_table (article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2) SELECT article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2 FROM ["""+webname+"""] WHERE article_id = ?""",current_aricle_id)
                            mydb.commit()
                            mydb.close()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("Update ["+webname+"] set approval_status = 'Move to Production' where article_id = ?",current_aricle_id)
                            mydb.commit()
                            mydb.close()
                        if(session['usertype'] == 'Admin' or session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("Update ["+webname+"] set approval_status = 'Sent for Approval' where article_id = ?",str(j[1]))
                            mydb.commit()
                            mydb.close()
                else:
                    flag = 0 
            if(flag == 1):
                fileupload = 'validfile'
                return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
            elif(flag == 0):
                fileupload = 'invalidwebsite'
                return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
        else:
            fileupload = 'invalidfile' 
            return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
        #     print(j[6])
            
        # mydb.close()
        # print(j[1])

@app.route('/fileupload1',methods = ['POST','GET'])
def fileupload1():
    if(request.method == 'POST'):
        webname = request.form.get('webname')
        pgid = request.form.get('pgid')
        f = request.files['file']
        inputdf = pd.read_excel(f)
        # inputdf.fillna('', inplace=True)
        shape = inputdf.shape
        headings_raw = ['Unnamed: 0', 'Article ID', 'Article Date', 'Healthcare Enterprise', 'Technology', 'Use Case', 'Vendor', 'Vendor Product', 'Speciality', 'Details', 'Article URL', 'Section Type', 'Approval Status', 'Rank', 'Vendor Count', 'Action: (U / A / D)']
        headings_dyn = list(inputdf.columns.values)
        print(headings_dyn)
        print(headings_raw)
        print(len(headings_raw))
        print(len(headings_dyn))
        flag = 0
        print(headings_raw==headings_dyn)
        if(headings_raw==headings_dyn):
            for i,j in inputdf.iterrows():
                if(str(j[11]) == webname):
                    flag = 1
                    if(j[15] == 'U'):
                        print('update')
                        if(session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update ["""+webname+"""] set article_date_website=?,Healthcare_Enterprise_Keyword=?,Technology_keyword=?,Use_Case_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_text=?,article_url=? where article_id=?""", (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[1])))
                            mydb.commit()
                        if(session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Updates' where article_id = ?""",str(j[1]))
                            print("""update ["""+webname+"""] set approval_status='Suggested Updates' where article_id = ?""",str(j[1]))
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",str(j[1]))
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],str(j[1])))
                            mydb.commit()
                    elif(j[15] == 'D'):
                        print('delete')
                        if(session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Deletions' where article_id = ?""",str(j[1]))
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",str(j[1]))
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],str(j[1])))
                            mydb.commit()
                    elif(j[15] == 'A'):
                        print('add')
                        print('Insert into production')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("select id from [" +webname+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                        webid_point = cursor1.fetchone()
                        current_aricle_id = webid_point[0]
                        Count = int(current_aricle_id)
                        cursor1.execute("select section_id from schema_mapping_data where section_name =? ",webname)
                        Value1 = cursor1.fetchone()
                        sid = Value1.section_id
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = 'INSERT INTO ['+ webname +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_id,section_type,article_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),sid,webname,sid + 'A' + str(Count+1))
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        if(session['usertype'] == 'Analyst'):
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select article_id from [" +webname+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            webid_point = cursor1.fetchone()
                            current_aricle_id = webid_point[0]
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Insertions' where article_id = ?""",current_aricle_id)
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,Healthcare_Enterprise_Keyword,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",current_aricle_id)
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],current_aricle_id))
                            mydb.commit()
                else:
                    print('invalid website')
                    flag = 0 
            if(flag == 1):
                fileupload = 'validfile'
                return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
            elif(flag == 0):
                fileupload = 'invalidwebsite'
                return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
        else:
            fileupload = 'invalidfile' 
            return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
           # return redirect('/Display?id='+webname+'&pgno='+pgid+'&valid='+fileupload)
@app.route('/fileupload2',methods = ['POST','GET'])
def fileupload2():
    if(request.method == 'POST'):
        webname = request.form.get('webname')
        pgid = request.form.get('pgid')
        f = request.files['file']
        inputdf = pd.read_excel(f)
        inputdf.fillna('', inplace=True)
        shape = inputdf.shape
        headings_raw = ['Unnamed: 0', 'Article ID', 'Article Date', 'Healthcare Enterprise', 'Technology', 'Use Case', 'Vendor', 'Vendor Product', 'Speciality', 'Details', 'Article URL', 'Section Type', 'Rank', 'Vendor Count','Table', 'Action: U / A / D']
        headings_dyn = list(inputdf.columns.values)
        print(headings_dyn)
        print(headings_raw)
        print(len(headings_raw))
        print(len(headings_dyn))
        flag = 0
        print(headings_raw==headings_dyn)
        if(headings_raw==headings_dyn):
            for i,j in inputdf.iterrows():
                if(str(j[14]) == webname):
                    flag = 1
                    if(j[15] == 'U'):
                        print('update')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("""update ["""+webname+"""] set article_date_website=?,Healthcare_Enterprise_Keyword=?,Technology_keyword=?,Use_Case_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_text=?,article_url=? where article_id=?""",(str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[1])))
                        mydb.commit()
                    elif(j[15] == 'D'):
                        print('delete')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute('delete from ['+webname+'] where article_id=?',str(j[1]))
                        mydb.commit()
                    elif(j[15] == 'A'):
                        print('add')
                        print('Insert into production')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        if(str(j[11] == 'Manual Upload')):
                            print('inside if')
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select id from [Manual Upload table] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            webid_point = cursor1.fetchone()
                            current_aricle_id = webid_point[0]
                            Count = int(current_aricle_id)
                            current_section_id = '04MU001'
                            val_website = 'Manual Upload table'
                        else:
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select id from [" +str(j[11])+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            webid_point = cursor1.fetchone()
                            current_aricle_id = webid_point[0]
                            Count = int(current_aricle_id)
                            cursor1.execute("select section_id from [" +str(j[11])+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            sectionid_point = cursor1.fetchone()
                            current_section_id = sectionid_point[0]
                            val_website = str(j[11])
                        # mydb = dbconnect()
                        # cursor1 = mydb.cursor()
                        # query1 = 'INSERT INTO ['+ webname +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,article_id,section_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        # val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),current_section_id + 'A' + str(Count+1),current_section_id)
                        # cursor1.execute(query1, val1)
                        # mydb.commit()
                        # mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = 'INSERT INTO ['+ val_website +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),current_section_id,current_section_id + 'A' + str(Count+1))
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("Update ["+val_website+"] set approval_status = 'Move to Production' where article_id = ?",current_section_id + 'A' + str(Count+1))
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = """INSERT INTO production_table (article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,table_name,article_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),str(j[14]),current_section_id + 'A' + str(Count+1))
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                else:
                    flag = 0 
            if(flag == 1):
                fileupload = 'validfile'
                return redirect('/Production_tab?pgno='+pgid+'&valid='+fileupload)
            elif(flag == 0):
                fileupload = 'invalidwebsite'
                return redirect('/Production_tab?pgno='+pgid+'&valid='+fileupload)
        else:
            fileupload = 'invalidfile' 
            return redirect('/Production_tab?pgno='+pgid+'&valid='+fileupload)

@app.route('/fileupload3',methods = ['POST','GET'])
def fileupload3():
    if(request.method == 'POST'):
        webname = 'Notification'
        pgid = request.form.get('pgid')
        f = request.files['file']
        inputdf = pd.read_excel(f)
        inputdf.fillna('', inplace=True)
        shape = inputdf.shape
        headings_raw = ['Unnamed: 0', 'Article ID', 'Article Date', 'Healthcare Enterprise', 'Technology', 'Use Case', 'Vendor', 'Vendor Product', 'Speciality', 'Details', 'Article URL', 'Section Type','Approval Status', 'Rank', 'Vendor Count','Table', 'Action: U / A / D']
        headings_dyn = list(inputdf.columns.values)
        print(headings_dyn)
        print(headings_raw)
        flag = 0
        print(headings_raw==headings_dyn)
        if(headings_raw==headings_dyn):
            for i,j in inputdf.iterrows():
                if(str(j[15]) == webname):
                    flag = 1
                    if(j[16] == 'U'):
                        print('update')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("""update ["""+str(j[11])+"""] set article_date_website=?,Healthcare_Enterprise_Keyword=?,Technology_keyword=?,Use_Case_Keyword=?,vendor_Keyword=?,vendor_product=?,speciality=?,article_text=?,article_url=? where article_id=?""", (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[1])))
                        mydb.commit()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute('delete from Notification where article_id=?',str(j[1]))
                        mydb.commit()
                    elif(j[16] == 'D'):
                        print('delete')
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute('delete from ['+str(j[11])+'] where article_id=?',str(j[1]))
                        mydb.commit()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute('delete from Notification where article_id=?',str(j[1]))
                        mydb.commit()
                    elif(j[16] == 'A'):
                        print('add')
                        print('Insert into production')
                        if(str(j[11] == 'Manual Upload')):
                            print('inside if')
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select id from [Manual Upload table] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            webid_point = cursor1.fetchone()
                            current_aricle_id = webid_point[0]
                            Count = int(current_aricle_id)
                            current_section_id = '04MU001'
                            val_website = 'Manual Upload table'
                        else:
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select id from [" +str(j[11])+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            webid_point = cursor1.fetchone()
                            current_aricle_id = webid_point[0]
                            Count = int(current_aricle_id)
                            cursor1.execute("select section_id from [" +str(j[11])+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
                            sectionid_point = cursor1.fetchone()
                            current_section_id = sectionid_point[0]
                            val_website = str(j[11])
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        print('DEBUG HERE')
                        print(webname)
                        print(str(j[11]))
                        print(current_section_id)
                        query1 = 'INSERT INTO ['+ webname +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,article_id,section_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),current_section_id + 'A' + str(Count+1),current_section_id)
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = 'INSERT INTO ['+ val_website +'](article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,article_id,section_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),current_section_id + 'A' + str(Count+1),current_section_id)
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute("Update ["+val_website+"] set approval_status = 'Move to Production' where article_id = ?",current_section_id + 'A' + str(Count+1))
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        query1 = """INSERT INTO production_table (article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,table_name,article_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
                        val1 = (str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7]),str(j[8]),str(j[9]),str(j[10]),str(j[11]),'production_table',current_section_id + 'A' + str(Count+1))
                        cursor1.execute(query1, val1)
                        mydb.commit()
                        mydb.close()
                        mydb = dbconnect()
                        cursor1 = mydb.cursor()
                        cursor1.execute('delete from Notification where article_id=?',str(j[1]))
                        mydb.commit()
                else:
                    flag = 0 
            if(flag == 1):
                fileupload = 'validfile'
                return redirect('/Notification_tab?pgno='+pgid+'&valid='+fileupload)
            elif(flag == 0):
                fileupload = 'invalidwebsite'
                return redirect('/Notification_tab?pgno='+pgid+'&valid='+fileupload)
        else:
            fileupload = 'invalidfile' 
            return redirect('/Notification_tab?pgno='+pgid+'&valid='+fileupload)


def Download_file_thread(webname,flag):
    mydb = dbconnect()
    cursor = mydb.cursor()
    rid = str(datetime.now().strftime('%d/%m/%Y , %H:%M:%S'))
    print(rid)
    filename = webname
    print(webname)
    print(flag)
    query1 = 'INSERT INTO Downloads(Username,Filename,Status,Referenceid) VALUES (?,?,?,?)'
    val1 = (flag,filename,'Scheduled to Download',rid)
    cursor.execute(query1, val1)
    mydb.commit()
    mydb = dbconnect()
    df = sql.read_sql("select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_Keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,approval_status,Rank,vendor_count from ["+webname+"]",mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_Keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_Keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','approval_status':'Approval Status','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df['Action: U / A / D'] = ''
    df.to_excel("static//files/"+ filename + ".xlsx")
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update Downloads set Status='Download' where Referenceid=?""", (rid))
    mydb.commit()


@app.route('/Download_file',methods = ['POST', 'GET'])
def Download_file():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data']
        flag = session['user']
        dt1 = Thread(target=Download_file_thread,args=(webname,flag))
        dt1.start()
        dt1.join()
        return {'websitename':webname}

@app.route('/Download_file_production',methods = ['POST', 'GET'])
def Download_file_production():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data']
        flag = session['user']
        dt1 = Thread(target=Download_file_production_thread,args=(webname,flag))
        dt1.start()
        dt1.join()
        return {'websitename':webname}

def Download_file_production_thread(webname,flag):
    mydb = dbconnect()
    cursor = mydb.cursor()
    rid = str(datetime.now().strftime('%d/%m/%Y , %H:%M:%S'))
    print(rid)
    filename = webname 
    print(webname)
    print(flag)
    query1 = 'INSERT INTO Downloads(Username,Filename,Status,Referenceid) VALUES (?,?,?,?)'
    val1 = (flag,filename,'Scheduled to Download',rid)
    cursor.execute(query1, val1)
    mydb.commit()
    mydb = dbconnect()
    df = sql.read_sql("select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_Keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,Rank,vendor_count,table_name from ["+webname+"]",mydb)
    df['Action: U / A / D'] = ''
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_Keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_Keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','table_name':'Table','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df.to_excel("static//files/"+ filename + ".xlsx")
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update Downloads set Status='Download' where Referenceid=?""", (rid))
    mydb.commit()






@app.route('/Download_singlepage_file',methods=['POST','GET'])
def Download_singlepage_file():
    webname = request.args.get('webname')
    webid = request.args.get('webid')
    mydb = dbconnect()
    print(webid)
    print(webname)
    df = sql.read_sql("select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,approval_status,Rank,vendor_count from ["+webname+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '') order by id OFFSET "+ str(webid) +" ROWS FETCH NEXT 10 ROWS ONLY",mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','approval_status':'Approval Status','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df['Action: (U / A / D)'] = ''
    filename = webname+'-from-id-'+webid+'-['+str(datetime.now().strftime('%d %m %Y , %H %M %S')) +']'
    df.to_excel("static//files/"+ filename + '.xlsx')
    file_path = 'static/files/'
    return send_from_directory(file_path,filename+'.xlsx', as_attachment=True)



@app.route('/Download_singlepage_file_production',methods=['POST','GET'])
def Download_singlepage_file_production():
    webname = request.args.get('webname')
    webid = request.args.get('webid')
    mydb = dbconnect()
    print(webid)
    print(webname)
    df = sql.read_sql("select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,Rank,vendor_count,table_name from ["+webname+"] order by id OFFSET "+ str(webid) +" ROWS FETCH NEXT 10 ROWS ONLY",mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','table_name':'Table','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df['Action: U / A / D'] = ''
    filename = webname+'-from-id-'+webid+'-['+str(datetime.now().strftime('%d %m %Y , %H %M %S')) +']'
    df.to_excel("static//files/"+ filename + '.xlsx')
    file_path = 'static/files/'
    return send_from_directory(file_path,filename+'.xlsx', as_attachment=True)

@app.route('/Download_singlepage_notification',methods=['POST','GET'])
def Download_singlepage_notification():
    webname = request.args.get('webname')
    webid = request.args.get('webid')
    mydb = dbconnect()
    print(webid)
    print(webname)
    df = sql.read_sql("select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,approval_status,Rank,vendor_count,table_name from ["+webname+"]",mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','table_name':'Table','section_type':'Section Type','vendor_count':'Vendor Count','approval_status':'Approval Status'}
    df.rename(columns=mydict,inplace=True)
    df['Action: U / A / D'] = ''
    filename = webname+'-from-id-'+webid+'-['+str(datetime.now().strftime('%d %m %Y , %H %M %S')) +']'
    df.to_excel("static//files/"+ filename + '.xlsx')
    file_path = 'static/files/'
    return send_from_directory(file_path,filename+'.xlsx', as_attachment=True)

@app.route('/Delete_single',methods = ['POST','GET'])
def Delete_single():
    val = request.get_json()
    print(val['data'])
    articleid = val['data']
    webname = val['data1']
    if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' ):
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute('Delete from ['+webname+'] where article_id = ?',articleid)
        mydb.commit()
        mydb.close()
        mydb = dbconnect()
        cursor3 = mydb.cursor()
        exist_query = cursor3.execute("""SELECT article_id FROM Notification where article_id =?""",(articleid))
        article_id_exist = cursor3.fetchone()
        if article_id_exist:
            aid = article_id_exist[0]
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute('Delete from Notification where article_id = ?',aid)
            mydb.commit()
            mydb.close()
    elif(session['usertype'] == 'Analyst'):
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Deletions' where article_id = ?""",articleid)
        mydb.commit()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",articleid)
        mydb.commit()
        cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],articleid))
        mydb.commit()
    return {'success':'true'}

@app.route('/Delete_multiple',methods = ['POST','GET'])
def Delete_multiple():
    if(request.method == 'POST'):
        value = request.get_json()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        webname = value['data1']
        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' ):
            for i in value['data']:
                cursor1.execute('Delete from ['+webname+'] where article_id = ?',i)
            mydb.commit()
            mydb.close()
            for i in value['data']:
                mydb = dbconnect()
                cursor3 = mydb.cursor()
                exist_query = cursor3.execute("""SELECT article_id FROM Notification where article_id =?""",(i))
                article_id_exist = cursor3.fetchone()
                if article_id_exist:
                    aid = article_id_exist[0]
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute('Delete from Notification where article_id = ?',aid)
                    mydb.commit()
                    mydb.close()
        elif(session['usertype'] == 'Analyst'):
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            for i in value['data']:
                cursor1.execute("""update ["""+webname+"""] set approval_status='Suggested Deletions' where article_id = ?""",i)
                mydb.commit()
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",i)
                mydb.commit()
                cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],i))
                mydb.commit()

    return {'success':'true'}

@app.route('/Delete_multiple_notify',methods = ['POST','GET'])
def Delete_multiple_notify():
    if(request.method == 'POST'):
        value = request.get_json()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        webname = value['data1']
        articlelist = value['data']
        if(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' ):
            for i in range(len(value['data'])):
                cursor1.execute('Delete from ['+webname[i]+'] where article_id = ?',articlelist[i])
            mydb.commit()
            mydb.close()
            for i in range(len(value['data'])):
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute('Delete from Notification where article_id = ?',articlelist[i])
                mydb.commit()
                mydb.close()
    return {'success':'true'}

@app.route('/Approve',methods = ['POST','GET'])
def Approve():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data1']
        for i in value['data']:
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("Update ["+webname+"] set approval_status = 'Sent for Approval' where article_id = ?",i)
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""INSERT INTO Notification (section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count) SELECT section_type,article_id,article_url,article_heading1,article_heading2,article_text,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_date_website,health_system,approval_status,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",i)
            mydb.commit()
            cursor1.execute("""update Notification set Suggested_by = ? where article_id = ?""",(session['user'],i))
            mydb.commit()
        mydb.close()
        return {'success':'true'}

@app.route('/Production',methods = ['POST','GET'])
def Production():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data1']
        approvedlist = []
        for i in value['data']:
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("Update ["+webname+"] set approval_status = 'Moved to Production' where article_id = ?",i)
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""INSERT INTO production_table (article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count) SELECT article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count FROM ["""+webname+"""] WHERE article_id = ?""",i)
            mydb.commit()
            mydb = dbconnect()
            cursor3 = mydb.cursor()
            exist_query = cursor3.execute("""SELECT article_id FROM Notification where article_id =?""",(i))
            article_id_exist = cursor3.fetchone()
            if article_id_exist:
                aid = article_id_exist[0]
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute('Delete from Notification where article_id = ?',aid)
                mydb.commit()
                mydb.close()
        return {'success':'true'}

@app.route('/Notify_to_Production',methods = ['POST','GET'])
def Notify_to_Production():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data1']
        articlelist = value['data']
        for i in range(len(value['data'])):
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("Update ["+webname[i]+"] set approval_status = 'Moved to Production' where article_id = ?",articlelist[i])
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""INSERT INTO production_table (article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count) SELECT article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_keyword,Use_Case_Keyword,vendor_keyword,vendor_product,speciality,article_text,article_url,section_type,section_id,article_heading1,article_heading2,Rank,vendor_count FROM ["""+webname[i]+"""] WHERE article_id = ?""",articlelist[i])
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute('Delete from Notification where article_id = ?',articlelist[i])
            mydb.commit()
            mydb.close()
        return {'success':'true'}

@app.route('/resetstatus')
def resetstatus():
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update schema_mapping_data set refresh_status = 'Need to Scrape' where refresh_status = 'Completed'""")
    mydb.commit()
    mydb.close()
    return redirect('/dashboard')


@app.route('/Notifystatus',methods = ['POST', 'GET'])
def Notifystatus():
    if(request.method == 'POST'):
        value = request.get_json()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        notifycount = cursor1.execute("""Select count(article_id) from """+ value['data'])
        result = cursor1.fetchone()
        print('Notify count is '+ str(result[0]))
        val = str(result[0])
        # print(val)
        mydb.close()
        return {'status':val}

@app.route('/arsearch',methods = ['POST','GET'])
def arsearch():
    if(request.method == 'POST'):
        webname = request.form.get('webname')
        searched_article = request.form.get('asearch')
        print('article is' + searched_article)
        searched_article = int(searched_article) - 1
        searched_article = searched_article * 10
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        d = cursor1.execute("select * from [" +webname+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '')  order by id OFFSET "+ str(searched_article) +" ROWS FETCH NEXT 10 ROWS ONLY")
        data = cursor1.fetchall()
        mydb.close()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        articlecount = cursor1.execute("Select count(*) from ["+webname+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '')")
        articlecount = cursor1.fetchone()
        articlecount = articlecount[0]
        print('A count is '+str(articlecount))
        pages = math.ceil(int(articlecount) / 10)
        if(session['usertype'] == 'Analyst'):
            return render_template('dashboard1.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})
        elif(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
            return render_template('dashboard2.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})
        elif( session['usertype'] == 'Admin'):
            return render_template('dashboard.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})

@app.route('/singlearsearch',methods = ['POST','GET'])
def singlearsearch():
    if(request.method == 'POST'):
        webname = request.form.get('webname')
        searched_article = request.form.get('artsearch')
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        d = cursor1.execute("select * from [" +webname+"] where article_id = ?",searched_article)
        data = cursor1.fetchall()
        mydb.close()
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        articlecount = cursor1.execute("Select count(*) from ["+webname+"] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '') ")
        articlecount = cursor1.fetchone()
        articlecount = articlecount[0]
        print('A count is '+str(articlecount))
        pages = math.ceil(int(articlecount) / 10)
        print(len(data))
        print(data)
        if(len(data) != 0):
            if(session['usertype'] == 'Analyst'):
                return render_template('dashboard1.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})
            elif(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
                return render_template('dashboard2.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})
            elif( session['usertype'] == 'Admin'):
                return render_template('dashboard.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':searched_article,'value':webname,'articlecount':articlecount,'noofpages':pages})
        else:
            pgid1 = 0
            fileupload = 'articlenotfound'
            return redirect('/Display?id='+webname+'&pgno='+str(pgid1)+'&valid='+fileupload)

@app.route('/keywords',methods=["POST",'GET'])
def keywords():
    filevalidity = request.args.get('valid')
    added_data = request.args.get('json')
    # print(added_data)
    if added_data is not None:
        added_data = json.loads(added_data)
        # print(added_data['Usecase_added'])
        # print(type(added_data))
        flag = 1
    else:
        added_data = 'None'
        flag = 0 
    mydb = dbconnect()
    cursor3 = mydb.cursor()
    cursor3.execute("select * from schema_mapping_data")
    data1 = cursor3.fetchall()
    return render_template('keywords.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd'],'filevalid':filevalidity,'data':data1,'uploadkey':added_data,'typeofuploadkey':flag})


@app.route('/Download_keywords')
def Download_keywords():
    mydb = dbconnect()
    df1=sql.read_sql("select id,Usecase,Status from Usecase",mydb)
    df1['Status: U / A / D'] = ''
    df2=sql.read_sql("select id,Technology,Status from Tech",mydb)
    df2['Status: U / A / D'] = ''
    df3=sql.read_sql("select id,Healthcare,Status from Healthcare",mydb)
    df3['Status: U / A / D'] = ''
    df4=sql.read_sql("select id,Vendor,Status from Vendor",mydb)
    df4['Status: U / A / D'] = ''
    writer = pd.ExcelWriter('static//files/Keywords.xlsx',engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Usecase',index=False)
    df2.to_excel(writer, sheet_name='Technology',index=False)
    df3.to_excel(writer, sheet_name='Healthcare enterprise',index=False)
    df4.to_excel(writer, sheet_name='Vendor',index=False)
    writer.save()
    file_path = 'static/files/'
    return send_from_directory(file_path,'Keywords.xlsx', as_attachment=True)

def keywordsdata():

    mydb = dbconnect()

    usecase_sql = "select Healthcare from Healthcare where status = 'Newly Added' "
    main_df = pd.read_sql_query(usecase_sql,mydb)
    Healthcare_new_keywords_added = (main_df.iloc[0:,0]).tolist()

    tech_sql = "select Technology from Tech where status = 'Newly Added'"
    main_df = pd.read_sql_query(tech_sql,mydb)
    Technology_new_keywords_added = (main_df.iloc[0:,0]).tolist()

    usecase_sql = "select UseCase from Usecase where status = 'Newly Added' "
    main_df = pd.read_sql_query(usecase_sql,mydb)
    Usecase_new_keywords_added = (main_df.iloc[0:,0]).tolist()

    vendor_sql = "select Vendor from Vendor where status = 'Newly Added' "
    main_df = pd.read_sql_query(vendor_sql,mydb)
    Vendor_new_keywords_added = (main_df.iloc[0:,0]).tolist()

    usecase_sql = "select Healthcare from Healthcare where status = 'Deleting' "
    main_df = pd.read_sql_query(usecase_sql,mydb)
    Healthcare_keywords_deleted = (main_df.iloc[0:,0]).tolist()

    tech_sql = "select Technology from Tech where status = 'Deleting'"
    main_df = pd.read_sql_query(tech_sql,mydb)
    Technology_keywords_deleted = (main_df.iloc[0:,0]).tolist()

    usecase_sql = "select UseCase from Usecase where status = 'Deleting' "
    main_df = pd.read_sql_query(usecase_sql,mydb)
    Usecase_keywords_deleted = (main_df.iloc[0:,0]).tolist()

    vendor_sql = "select Vendor from Vendor where status = 'Deleting' "
    main_df = pd.read_sql_query(vendor_sql,mydb)
    Vendor_keywords_deleted = (main_df.iloc[0:,0]).tolist()

    return Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,Vendor_new_keywords_added,Healthcare_keywords_deleted,Technology_keywords_deleted,Usecase_keywords_deleted,Vendor_keywords_deleted

def keywordmapmain(l1,l2,l3,l4,l5,l6,webname):
        print('started into main function')
        for i in range(len(l1)):
            Healthcare_list = []
            Technology_list = []
            Usecase_list = []
            vendor_list = []
            if len(l2) != 0 :
                # print(' in Healthcare')
                for j in l2:
                    if(str(j).isupper()):
                        if(str(j) in str(l1[i])):
                            Healthcare_list.append(str(j))
                    else:
                        if(str(j).lower() in str(l1[i]).lower()):
                            Healthcare_list.append(str(j))

                if(len(Healthcare_list) == 0):
                    Healthcare_string = ''
                else:
                    Healthcare_string = ",".join(Healthcare_list)
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update [""" +webname+ """] set Healthcare_Enterprise_Keyword = ? where article_id = ?""",(Healthcare_string,l5[i]))
                    mydb.commit()
            else:
                print('not in helthcare')
            if len(l3) != 0 :
                for k in l3:
                    if(str(k).isupper()):
                        if(str(k) in str(l1[i])):
                            Technology_list.append(str(k))
                    else:
                        if(str(k).lower() in str(l1[i]).lower()):
                            Technology_list.append(str(k))

                if(len(Technology_list) == 0):
                    Technology_string = ''
                else:
                    # print('inside else healthcare')
                    # print(Technology_list)
                    Technology_string = ",".join(Technology_list)
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update [""" +webname+ """] set Technology_Keyword = ? where article_id = ?""",(Technology_string,l5[i]))
                    mydb.commit()
            if len(l4) != 0 :
                for l in l4:
                    if(str(l).isupper()):
                        if(str(l) in str(l1[i])):
                            Usecase_list.append(str(l))
                    else:
                        if(str(l).lower() in str(l1[i]).lower()):
                            Usecase_list.append(str(l))
                if(len(Usecase_list) == 0):
                    Usecase_string = ''
                else:
                    Usecase_string = ",".join(Usecase_list)
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update [""" +webname+ """] set Use_Case_Keyword = ? where article_id = ?""",(Usecase_string,l5[i]))
                    mydb.commit()

            if len(l6) != 0 :
                for m in l6:
                    if(str(m).isupper()):
                        if(" " + str(m) + " " in str(l1[i])):
                            vendor_list.append(str(m))
                    else:
                        if(" " + str(m) + " "  in str(l1[i])):
                            vendor_list.append(str(m))
                if(len(vendor_list) == 0):
                    vendor_string = ''
                else:
                    # print('vendor list not empty')
                    vendor_string = ",".join(vendor_list)
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""update [""" +webname+ """] set vendor_Keyword = ? where article_id = ?""",(vendor_string,l5[i]))
                    mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update [""" +webname+ """] set Rank = ? where article_id = ?""",(len(Usecase_list)+len(Technology_list),l5[i]))
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update [""" +webname+ """] set vendor_count = ? where article_id = ?""",(len(vendor_list),l5[i]))
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update [""" +webname+ """] set Mapped_status = 'Mapped' where article_id = ?""",(l5[i]))
            mydb.commit()
        return 'done'

def deletekeywords(oldarticlesid,Healthcare_keywords_deleted,Technology_keywords_deleted,Vendor_keywords_deleted,Usecase_keywords_deleted,webname):
    print('No of articles to get remapped:',len(oldarticlesid))
    for i in range(len(oldarticlesid)):
        print(oldarticlesid[i])
        if len(Healthcare_keywords_deleted) != 0 :
            print('Healthcare keywords are present to delete')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select Healthcare_Enterprise_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
            Value1 = cursor1.fetchone()
            Healthcare_value = Value1.Healthcare_Enterprise_Keyword
            if(type(Healthcare_value) is str):
                Healthcare_list = Healthcare_value.split(",")
                for k in Healthcare_keywords_deleted:
                    for j in Healthcare_list:
                        if  str(k) in str(j):
                            Healthcare_list.remove(k)
                            Healthcare_string_value = ",".join(Healthcare_list)
                            cursor1.execute("""update [""" +webname+ """] set Healthcare_Enterprise_Keyword = ? where article_id = ?""",(Healthcare_string_value,oldarticlesid[i]))
                            mydb.commit()
        if len(Technology_keywords_deleted) != 0 :
            print('Tech keywords are present to delete')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
            Value1 = cursor1.fetchone()
            Technology_value = Value1.Technology_Keyword
            if(type(Technology_value) is str):
                Technology_list = Technology_value.split(",")
                for k in Technology_keywords_deleted:
                    for j in Technology_list:
                        if  str(k) in str(j):
                            Technology_list.remove(k)
                            Technology_string_value = ",".join(Technology_list)
                            cursor1.execute("""update [""" +webname+ """] set Technology_Keyword = ? where article_id = ?""",(Technology_string_value,oldarticlesid[i]))
                            mydb.commit()

                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
                            Value1 = cursor1.fetchone()
                            Usecase_value = Value1.Use_Case_Keyword

                            if(Usecase_value is None or Usecase_value == ''):
                                Usecase_count = 0
                            else:
                                Usecase_count = len(Usecase_value.split(","))
                            cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
                            Value1 = cursor1.fetchone()
                            Technology_value = Value1.Technology_Keyword

                            if(Technology_value is None or Technology_value == ''):
                                Technology_count = 0
                            else:
                                Technology_count = len(Technology_value.split(","))

                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update [""" +webname+ """] set Rank = ? where article_id = ?""",(Usecase_count+Technology_count,oldarticlesid[i]))
                            mydb.commit()

        if len(Vendor_keywords_deleted) != 0 :
            print('Vendor keywords are present to delete')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select vendor_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
            Value1 = cursor1.fetchone()
            vendor_value = Value1.vendor_Keyword
            if(type(vendor_value) is str):
                vendor_list = vendor_value.split(",")
                for k in Vendor_keywords_deleted:
                    for j in vendor_list:
                        if  str(k) in str(j):
                            vendor_list.remove(k)
                            vendor_string_value = ",".join(vendor_list)
                            cursor1.execute("""update [""" +webname+ """] set vendor_Keyword = ? where article_id = ?""",(vendor_string_value,oldarticlesid[i]))
                            mydb.commit()
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("select vendor_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
                            Value1 = cursor1.fetchone()
                            vendor_value = Value1.vendor_Keyword
                            if(vendor_value is None or vendor_value == ''):
                                vendor_count = 0
                            else:
                                vendor_count = len(vendor_value.split(","))
                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update [""" +webname+ """] set vendor_count = ? where article_id = ?""",(vendor_count,oldarticlesid[i]))
                            mydb.commit()
        if len(Usecase_keywords_deleted) != 0 :
            print('Usecase keywords are present to delete')
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
            Value1 = cursor1.fetchone()
            Usecase_value = Value1.Use_Case_Keyword
            if(type(Usecase_value) is str):
                Usecase_list = Usecase_value.split(",")
                for k in Usecase_keywords_deleted:
                    for j in Usecase_list:
                        if  str(k) in str(j):
                            Usecase_list.remove(k)
                            Usecase_string_value = ",".join(Usecase_list)
                            cursor1.execute("""update [""" +webname+ """] set Use_Case_Keyword = ? where article_id = ?""",(Usecase_string_value,oldarticlesid[i]))
                            mydb.commit()

                            mydb = dbconnect()
                            cursor1 = mydb.cursor()

                            cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
                            Value1 = cursor1.fetchone()
                            Usecase_value = Value1.Use_Case_Keyword

                            if(Usecase_value is None or Usecase_value == ''):
                                Usecase_count = 0
                            else:
                                Usecase_count = len(Usecase_value.split(","))
                            cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",oldarticlesid[i])
                            Value1 = cursor1.fetchone()
                            Technology_value = Value1.Technology_Keyword

                            if(Technology_value is None or Technology_value == ''):
                                Technology_count = 0
                            else:
                                Technology_count = len(Technology_value.split(","))

                            mydb = dbconnect()
                            cursor1 = mydb.cursor()
                            cursor1.execute("""update [""" +webname+ """] set Rank = ? where article_id = ?""",(Usecase_count+Technology_count,oldarticlesid[i]))
                            mydb.commit()

     



        
        # mydb = dbconnect()
        # cursor1 = mydb.cursor()
        # cursor1.execute("""update [""" +webname+ """] set Mapped_status = 'Mapped' where article_id = ?""",(l5[i]))
        # mydb.commit()


                





def keywordmapmain1(l1,l2,l3,l4,l5,l6,webname):
    print(l4)
    print(l2)
    for i in range(len(l5)):
        Healthcare_list = []
        Technology_list = []
        Usecase_list = []
        vendor_list = []
        if len(l2) != 0 :
            print('Healthcare keyword added')
            for j in l2:
                if(str(j).isupper()):
                    if(str(j) in str(l1[i])):
                        Healthcare_list.append(str(j))
                else:
                    if(str(j).lower() in str(l1[i]).lower()):
                        Healthcare_list.append(str(j))

            if(len(Healthcare_list) == 0):
                Healthcare_string = ''
            else:
                Healthcare_string = ",".join(Healthcare_list)
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select Healthcare_Enterprise_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Healthcare_value = Value1.Healthcare_Enterprise_Keyword

                if(Healthcare_value is None or Healthcare_value == ''):
                    cursor1.execute("""update [""" +webname+ """] set Healthcare_Enterprise_Keyword = ? where article_id = ?""",(Healthcare_string,l5[i]))
                    mydb.commit()
                else:
                    cursor1.execute("""update [""" +webname+ """] set Healthcare_Enterprise_Keyword = Healthcare_Enterprise_Keyword +',' + ?  where article_id = ?""",(Healthcare_string,l5[i]))
                    mydb.commit()


        if len(l3) != 0 :
            for k in l3:
                if(str(k).isupper()):
                    if(str(k) in str(l1[i])):
                        Technology_list.append(str(k))
                else:
                    if(str(k).lower() in str(l1[i]).lower()):
                        Technology_list.append(str(k))

            if(len(Technology_list) == 0):
                Technology_string = ''
            else:
                Technology_string = ",".join(Technology_list)
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Technology_value = Value1.Technology_Keyword

                if(Technology_value is None or Technology_value == ''):
                    cursor1.execute("""update [""" +webname+ """] set Technology_Keyword = ? where article_id = ?""",(Technology_string,l5[i]))
                    mydb.commit()
                else:
                    cursor1.execute("""update [""" +webname+ """] set Technology_Keyword = Technology_Keyword + ',' + ? where article_id = ?""",(Technology_string,l5[i]))
                    mydb.commit()

                cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Usecase_value = Value1.Use_Case_Keyword

                if(Usecase_value is None or Usecase_value == ''):
                    Usecase_count = 0
                else:
                    Usecase_count = len(Usecase_value.split(","))

                cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Technology_value = Value1.Technology_Keyword

                if(Technology_value is None or Technology_value == ''):
                    Technology_count = 0
                else:
                    Technology_count = len(Technology_value.split(","))


                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update [""" +webname+ """] set Rank = ? where article_id = ?""",(Usecase_count+Technology_count,l5[i]))
                mydb.commit()
                print('done')


        if len(l4) != 0 :
            for l in l4:
                if(str(l).isupper()):
                    if(str(l) in str(l1[i])):
                        Usecase_list.append(str(l))
                else:
                    if(str(l).lower() in str(l1[i]).lower()):
                        Usecase_list.append(str(l))
            if(len(Usecase_list) == 0):
                Usecase_string = ''
            else:
                Usecase_string = ",".join(Usecase_list)
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Usecase_value = Value1.Use_Case_Keyword
                if(Usecase_value is None or Usecase_value == ''):
                    cursor1.execute("""update [""" +webname+ """] set Use_Case_Keyword = ? where article_id = ?""",(Usecase_string,l5[i]))
                    mydb.commit()
                else:
                    cursor1.execute("""update [""" +webname+ """] set Use_Case_Keyword = Use_Case_Keyword + ',' + ? where article_id = ?""",(Usecase_string,l5[i]))
                    mydb.commit()

                cursor1.execute("select Use_Case_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Usecase_value = Value1.Use_Case_Keyword

                if(Usecase_value is None or Usecase_value == ''):
                    Usecase_count = 0
                else:
                    Usecase_count = len(Usecase_value.split(","))

                cursor1.execute("select Technology_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                Technology_value = Value1.Technology_Keyword

                if(Technology_value is None or Technology_value == ''):
                    Technology_count = 0
                else:
                    Technology_count = len(Technology_value.split(","))

                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update [""" +webname+ """] set Rank = ? where article_id = ?""",(Usecase_count+Technology_count,l5[i]))
                mydb.commit()
                print('done')



        if len(l6) != 0 :
            for m in l6:
                if(str(m).isupper()):
                    if(" " + str(m) + " " in str(l1[i])):
                        vendor_list.append(str(m))
                else:
                    if(" " + str(m) + " "  in str(l1[i])):
                        vendor_list.append(str(m))
            if(len(vendor_list) == 0):
                vendor_string = ''
            else:
                # print('vendor list not empty')
                vendor_string = ",".join(vendor_list)
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select vendor_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                vendor_value = Value1.vendor_Keyword
                if(vendor_value is None or vendor_value == ''):
                    cursor1.execute("""update [""" +webname+ """] set vendor_Keyword = ? where article_id = ?""",(vendor_string,l5[i]))
                    mydb.commit()
                else:
                    cursor1.execute("""update [""" +webname+ """] set vendor_Keyword = vendor_Keyword + ',' + ?  where article_id = ?""",(vendor_string,l5[i]))
                    mydb.commit()

                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("select vendor_Keyword from [" + webname + "]  where article_id =? ",l5[i])
                Value1 = cursor1.fetchone()
                vendor_value = Value1.vendor_Keyword
                if(vendor_value is None or vendor_value == ''):
                    vendor_count = 0
                else:
                    vendor_count = len(vendor_value.split(","))

                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update [""" +webname+ """] set vendor_count = ? where article_id = ?""",(vendor_count,l5[i]))
                mydb.commit()


        # mydb = dbconnect()
        # cursor1 = mydb.cursor()
        # cursor1.execute("""update [""" +webname+ """] set Mapped_status = 'Mapped' where article_id = ?""",(l5[i]))
        # mydb.commit()
    return 'done'

@app.route('/Keywordmap',methods = ['POST', 'GET'])
def Keywordmap():
    if(request.method == 'POST'):
        webname = request.get_json()
        condition = webname['data1']
        condition.pop(0)
        webname_string = ",".join(condition)
        weblist = webname['data2']
        print(weblist)
        print(type(weblist))
        if(type(weblist) is str):
            webelement = weblist
            weblist = []
            weblist.append(webelement)
            print('no')
        else:
            print('it is a list')
        for webname in weblist:
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set mapping_status='In Queue' where section_name=?""",webname)
            mydb.commit()

        Keywordmapthreadvariable = Thread(target=Keywordmapthread, args=(weblist,condition))
        Keywordmapthreadvariable.start()
        Keywordmapthreadvariable.join()

    return redirect('/keywords')



def Keywordmapthread(weblist,condition):

    for webname in weblist:
        # print(webname)
        threads = []

        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update schema_mapping_data set mapping_status='In progress' where section_name=?""",webname)
        mydb.commit()

        Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,Vendor_new_keywords_added,Healthcare_keywords_deleted,Technology_keywords_deleted,Usecase_keywords_deleted,Vendor_keywords_deleted = keywordsdata()

        if(len(condition) != 0):
            aid_sql = "select article_id from ["+webname+"] where  Mapped_status is NULL and approval_status in ("+webname_string+") order by id "
            main_df = pd.read_sql_query(aid_sql,mydb)
            newarticlesid = (main_df.iloc[0:,0]).tolist()
        else:
            aid_sql = "select article_id from ["+webname+"] where  Mapped_status is NULL order by id "
            main_df = pd.read_sql_query(aid_sql,mydb)
            newarticlesid = (main_df.iloc[0:,0]).tolist()


        print(len(newarticlesid))

        if len(newarticlesid) != 0:

            if(len(condition) != 0):
                article_sql = "SELECT  article_text from [" + webname + "] where Mapped_status is NULL and approval_status in ("+webname_string+") order by id "
                main_df = pd.read_sql_query(article_sql,mydb)
                newarticles = (main_df.iloc[0:,0]).tolist()
            else:
                aid_sql = "select article_text from [" +webname+"] where  Mapped_status is NULL order by id "
                main_df = pd.read_sql_query(aid_sql,mydb)
                newarticles = (main_df.iloc[0:,0]).tolist()

            usecase_sql = "select Healthcare from Healthcare where status = 'Active'"
            main_df = pd.read_sql_query(usecase_sql,mydb)
            Healthcare_old_keywords = (main_df.iloc[0:,0]).tolist()

            tech_sql = "select Technology from Tech where status = 'Active'"
            main_df = pd.read_sql_query(tech_sql,mydb)
            Technology_old_keywords = (main_df.iloc[0:,0]).tolist()

            health_sql = "select UseCase from Usecase where status = 'Active' "
            main_df = pd.read_sql_query(health_sql,mydb)
            Usecase_old_keywords = (main_df.iloc[0:,0]).tolist()

            vendor_sql = "select Vendor from Vendor where status = 'Active'"
            main_df = pd.read_sql_query(vendor_sql,mydb)
            Vendor_old_keywords = (main_df.iloc[0:,0]).tolist()

            # keywordmapmain(newarticles,Healthcare_old_keywords,Technology_old_keywords,Usecase_old_keywords,newarticlesid,Vendor_old_keywords,webname)
            keywordmapmainthread = Thread(target=keywordmapmain, args=(newarticles,Healthcare_old_keywords,Technology_old_keywords,Usecase_old_keywords,newarticlesid,Vendor_old_keywords,webname))
            keywordmapmainthread.start()
            keywordmapmainthread.join()

            # keywordmapmain1(newarticles,Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,newarticlesid,Vendor_new_keywords_added,webname)
            keywordmapmainthread1 = Thread(target=keywordmapmain1, args=(newarticles,Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,newarticlesid,Vendor_new_keywords_added,webname))
            keywordmapmainthread1.start()
            keywordmapmainthread1.join()

        
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("select mapping_status_newkeywords from schema_mapping_data where section_name=?",(webname))
        v1 = cursor1.fetchone()
        mapstatus = v1.mapping_status_newkeywords
        # print(mapstatus)

        if mapstatus != 'Searched':
            # print('inside')

            aid_sql = "select article_id from [" +webname+ "] where  Mapped_status = 'Mapped' order by id "
            main_df = pd.read_sql_query(aid_sql,mydb)
            oldarticlesid = (main_df.iloc[0:,0]).tolist()

            if(len(Healthcare_keywords_deleted)+len(Technology_keywords_deleted)+len(Vendor_keywords_deleted)+len(Usecase_keywords_deleted) != 0):
                print('delete started')
                deletekeywords(oldarticlesid,Healthcare_keywords_deleted,Technology_keywords_deleted,Vendor_keywords_deleted,Usecase_keywords_deleted,webname)
                deletekeywordsthread= Thread(target=deletekeywords, args=(oldarticlesid,Healthcare_keywords_deleted,Technology_keywords_deleted,Vendor_keywords_deleted,Usecase_keywords_deleted,webname))
                deletekeywordsthread.start()
                deletekeywordsthread.join()
                # threads.append(deletekeywordsthread)

            if(len(Healthcare_new_keywords_added)+len(Technology_new_keywords_added)+len(Vendor_new_keywords_added)+len(Usecase_new_keywords_added) != 0):

                article_sql = "SELECT  article_text from [" + webname + "] where Mapped_status = 'Mapped' order by id "
                main_df = pd.read_sql_query(article_sql,mydb)
                oldarticles = (main_df.iloc[0:,0]).tolist()

                print('inside adding new keywords for older articles')
                # keywordmapmain1(oldarticles,Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,oldarticlesid,Vendor_new_keywords_added,webname)
                keywordmapmain2= Thread(target=keywordmapmain1, args=(oldarticles,Healthcare_new_keywords_added,Technology_new_keywords_added,Usecase_new_keywords_added,oldarticlesid,Vendor_new_keywords_added,webname))
                keywordmapmain2.start()
                keywordmapmain2.join()
                # threads.append(keywordmapmain2)

            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update schema_mapping_data set mapping_status_newkeywords='Searched' where section_name=?""",webname)
            mydb.commit()





        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("""update schema_mapping_data set mapping_status='Mapped' where section_name=?""",webname)
        mydb.commit()

    return redirect('/keywords')
    
@app.route('/Upload_keywords',methods = ['POST', 'GET'])
def Upload_keywords():
    if(request.method == 'POST'):
        f = request.files['file']
        xl = pd.ExcelFile(f)
        keyword_tables = xl.sheet_names
        if ('Usecase' in keyword_tables and 'Technology' in keyword_tables and 'Healthcare enterprise' in keyword_tables and 'Vendor' in keyword_tables):
            df1 = pd.read_excel(f, sheet_name = 'Usecase')
            df2 = pd.read_excel(f, sheet_name = 'Technology')
            df3 = pd.read_excel(f, sheet_name = 'Healthcare enterprise')
            df4 = pd.read_excel(f, sheet_name = 'Vendor')
            Usecase_added = []
            Usecase_deleted = []
            Technology_added = []
            Technology_deleted = []
            Healthcare_enterprise_added = []
            Healthcare_enterprise_deleted = []
            Vendor_added = []
            Vendor_deleted = []
            for i,j in df3.iterrows():
                if j[3] == 'A':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    query1 = 'INSERT INTO Healthcare (Healthcare,Status) VALUES (?,?)'
                    val1 = (str(j[1]),'Newly Added')
                    cursor1.execute(query1, val1)
                    mydb.commit()
                if j[3] == 'D':
                    Healthcare_enterprise_deleted.append(str(j[1]))
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("Update Healthcare set Status = 'Deleting' where ID = ?",j[0])
                    mydb.commit()
                    mydb.close()
                if j[3] == 'U':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""Update Healthcare set Healthcare =? , Status = 'Newly Added' where ID = ?""",(j[1],j[0]))
                    mydb.commit()
                    mydb.close()
            for i,j in df2.iterrows():
                if j[3] == 'A':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    query1 = 'INSERT INTO Tech (Technology,Status) VALUES (?,?)'
                    val1 = (str(j[1]),'Newly Added')
                    cursor1.execute(query1, val1)
                    mydb.commit()
                if j[3] == 'D':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("Update Tech set Status = 'Deleting' where ID = ?",j[0])
                    mydb.commit()
                    mydb.close()
                if j[3] == 'U':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""Update Tech set Technology =? , Status = 'Newly Added' where id = ?""",(j[1],j[0]))
                    mydb.commit()
                    mydb.close()
            for i,j in df1.iterrows():
                if j[3] == 'A':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    query1 = 'INSERT INTO Usecase (Usecase,Status) VALUES (?,?)'
                    val1 = (str(j[1]),'Newly Added')
                    cursor1.execute(query1, val1)
                    mydb.commit()
                if j[3] == 'D':
                    Usecase_deleted.append(str(j[1]))
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    print()
                    cursor1.execute("Update Usecase set Status = 'Deleting' where ID = ?",j[0])
                    mydb.commit()
                    mydb.close()
                if j[3] == 'U':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""Update Usecase set Usecase =? , Status = 'Newly Added' where ID = ?""",(j[1],j[0]))
                    mydb.commit()
                    mydb.close()
            for i,j in df4.iterrows():
                if j[3] == 'A':
                    Vendor_added.append(str(j[1]))
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    query1 = 'INSERT INTO vendor (Vendor,Status) VALUES (?,?)'
                    val1 = (str(j[1]),'Newly Added')
                    cursor1.execute(query1, val1)
                    mydb.commit()
                if j[3] == 'D':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("Update Vendor set Status = 'Deleting' where ID = ?",j[0])
                    mydb.commit()
                    mydb.close()
                if j[3] == 'U':
                    mydb = dbconnect()
                    cursor1 = mydb.cursor()
                    cursor1.execute("""Update Vendor set Vendor =? , Status = 'Newly Added' where ID = ?""",(j[1],j[0]))
                    mydb.commit()
                    mydb.close()
            fileupload = 'validfile'
            # return redirect(url_for('.keywords', valid=fileupload))
            # myd = {"Usecase_added":Usecase_added,"Usecase_deleted":Usecase_deleted,"Vendor_added":Vendor_added,"Vendor_deleted":Vendor_deleted,"Healthcare_enterprise_added":Healthcare_enterprise_added,"Healthcare_enterprise_deleted":Healthcare_enterprise_deleted,"Technology_added":Technology_added,"Technology_deleted":Technology_deleted}
            # myd = json.dumps(myd, indent = 4) 
            return redirect('/keywords?valid='+fileupload)
        else:
            fileupload = 'invalidfile'
            # return redirect(url_for('.keywords', valid=fileupload))
            return redirect('/keywords?valid='+fileupload)


def Downloadacceptedthread(webname,flag):
    mydb = dbconnect()
    cursor = mydb.cursor()
    rid = str(datetime.now().strftime('%d/%m/%Y , %H:%M:%S'))
    print(rid)
    filename = webname + '_accepted'
    print(webname)
    print(flag)
    query1 = 'INSERT INTO Downloads(Username,Filename,Status,Referenceid) VALUES (?,?,?,?)'
    val1 = (flag,filename,'Scheduled to Download',rid)
    cursor.execute(query1, val1)
    mydb.commit()
    mydb = dbconnect()
    df = sql.read_sql("Select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_Keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,approval_status,Rank,vendor_count from ["""+webname+"""] where Rank > 0 and vendor_count > 0 and (Healthcare_Enterprise_Keyword is not Null and Healthcare_Enterprise_Keyword != '')  """,mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_Keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_Keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','approval_status':'Approval Status','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df['Action: (U / A / D)'] = ''
    df.to_excel("static//files/"+ filename + ".xlsx")
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update Downloads set Status='Download' where Referenceid=?""", (rid))
    mydb.commit()


@app.route('/Downloadaccepted',methods = ['POST', 'GET'])
def Downloadaccepted():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data']
        flag = session['user']
        dt1 = Thread(target=Downloadacceptedthread,args=(webname,flag))
        dt1.start()
        dt1.join()
        return {'websitename':webname}

@app.route('/Down',methods = ['POST', 'GET'])
def Down():
    filename = request.args.get('webname')
    file_path = 'static/files/'
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update Downloads set status='Downloaded' where filename = ?""",filename)
    mydb.commit()
    return send_from_directory(file_path,filename+'.xlsx', as_attachment=True)

@app.route('/downloadstab')
def downloadstab():
    mydb = dbconnect()
    cursor3 = mydb.cursor()
    cursor3.execute("select * from Downloads where status !='Downloaded' and Username = ?",session['user'])
    data1 = cursor3.fetchall()
    return render_template('Downloads.php',variable={'username': session['user'],'usertype': session['usertype'],'password':session['pwd'],'data':data1})



def Downloadrejectedthread(webname,flag):
    mydb = dbconnect()
    cursor = mydb.cursor()
    rid = str(datetime.now().strftime('%d/%m/%Y , %H:%M:%S'))
    print(rid)
    filename = webname + '_rejected'
    print(webname)
    print(flag)
    query1 = 'INSERT INTO Downloads(Username,Filename,Status,Referenceid) VALUES (?,?,?,?)'
    val1 = (flag,filename,'Scheduled to Download',rid)
    cursor.execute(query1, val1)
    mydb.commit()
    mydb = dbconnect()
    df = sql.read_sql("Select article_id,article_date_website,Healthcare_Enterprise_Keyword,Technology_Keyword,Use_Case_Keyword,vendor_Keyword,vendor_product,speciality,article_text,article_url,section_type,approval_status,Rank,vendor_count from ["""+webname+"""] where Rank < 1 or vendor_count < 1 or (Healthcare_Enterprise_Keyword is Null or Healthcare_Enterprise_Keyword = '')  """,mydb)
    mydict = {'article_id': 'Article ID','article_date_website': 'Article Date','Healthcare_Enterprise_Keyword': 'Healthcare Enterprise','Technology_Keyword':'Technology','Use_Case_Keyword':'Use Case','vendor_product':'Vendor Product','vendor_Keyword':'Vendor','speciality':'Speciality','article_text':'Details','article_url':'Article URL','approval_status':'Approval Status','section_type':'Section Type','vendor_count':'Vendor Count'}
    df.rename(columns=mydict,inplace=True)
    df['Action: (U / A / D)'] = ''
    df.to_excel("static//files/"+ filename + ".xlsx")
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    cursor1.execute("""update Downloads set Status='Download' where Referenceid=?""", (rid))
    mydb.commit()

@app.route('/Downloadrejected',methods = ['POST', 'GET'])
def Downloadrejected():
    if(request.method == 'POST'):
        value = request.get_json()
        webname = value['data']
        flag = session['user']
        dt1 = Thread(target=Downloadrejectedthread,args=(webname,flag))
        dt1.start()
        dt1.join()
        return {'websitename':webname}
       





@app.route('/resetstatuskeywords',methods = ['POST', 'GET'])
def resetstatuskeywords():
    if(request.method == 'POST'):
        mydb = dbconnect()
        cursor1 = mydb.cursor()
        cursor1.execute("select count(mapping_status_newkeywords) from schema_mapping_data where mapping_status_newkeywords = 'Mapped'")
        v1 = cursor1.fetchone()
        val = int(str(v1[0]))
        flag = 0
        if val >= 40:
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Tech set Technology = 'Inactive' where Technology = 'Deleting'""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Usecase set Usecase = 'Inactive' where Usecase = 'Deleting'""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Healthcare set Technology = 'Inactive' where Healthcare = 'Deleting'""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Vendor set Technology = 'Inactive' where Vendor = 'Deleting'""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Tech set Technology = 'Active' where Technology = 'Newly Added'""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Usecase set Usecase = 'Active' where Usecase = 'Newly Added''""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Healthcare set Technology = 'Active' where Healthcare = 'Newly Added''""")
            mydb.commit()
            mydb = dbconnect()
            cursor1 = mydb.cursor()
            cursor1.execute("""update Vendor set Technology = 'Active' where Vendor = 'Newly Added''""")
            mydb.commit()
            mydb.close()
            flag = 1
        return {'status':flag}


#Step -7(run the app)
if __name__ == '__main__':
    app.run(debug=True)