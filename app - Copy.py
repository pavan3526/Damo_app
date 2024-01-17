#Step – 1(import necessary library)

# Message Box

from flask import (Flask, flash, redirect, render_template, request, session, abort)
import pyodbc 
from datetime import date
import pandas as pd
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import os

import datetime
from datetime import date


def dbconnect():
    mydb = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=database-3.c1tcw6ocvqyh.us-east-1.rds.amazonaws.com;"
                        "Database=damo;"
                        "uid=Damo;pwd=Damo2021")
    return mydb
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
            mydb = dbconnect()
            cursor = mydb.cursor()
            role = cursor.execute("""SELECT (role) FROM users where username =? and password=?""",(session['user'],session['pwd']))
            user_role = cursor.fetchone()
            session['usertype'] = user_role[0]
            return redirect('/dashboard')
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html',msg = msg)
    return render_template("login.html",variable="Incorrect password or User doesn't exist")

#Step -5(creating route for dashboard and logout)
@app.route('/dashboard')
def dashboard():
    mydb = dbconnect()
    logintime = datetime.now()
    cursor1 = mydb.cursor()
    cursor1.execute("""update users set last_loggedin=? where username=?""", (logintime, session['user']))
    mydb.commit()
    mydb.close()
    mydb = dbconnect()
    cursor2 = mydb.cursor()
    cursor2.execute("select * from schema_mapping_data")
    data1 = cursor2.fetchall()
    return render_template("Scraper.php",variable={'username': session['user'],'usertype': session['usertype'],'data':data1})


@app.route('/Scraper')
def Scraper():
    mydb = dbconnect()
    cursor3 = mydb.cursor()
    cursor3.execute("select * from schema_mapping_data")
    data1 = cursor3.fetchall()
    cursor3.execute('select last_refreshed_on from schema_mapping_data')
    value = cursor3.fetchall()
    lastrefarray = []
    print(value)
    for d in value:
        today = date.today()
        delta = today - d[0].date()

        if delta.days > 14:
            lastrefarray.append('Yes')
        else:
            lastrefarray.append('No')

    if(session['usertype'] == 'Admin' or session['usertype'] == 'Analyst' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Approver'):
        return render_template('Scraper.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1,'data2':lastrefarray})
    else:
        return render_template('login.html')

@app.route('/View')
def View():
    mydb = dbconnect()
    cursor3 = mydb.cursor()
    cursor3.execute("select * from schema_mapping_data")
    data1 = cursor3.fetchall()
    if(session['usertype'] == 'Analyst' or session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin' or session['usertype'] == 'Admin' ):
        return render_template('View.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data1})
    else:
        return render_template('login.html')



@app.route('/Display')
def Display():
    value = request.args.get('id')
    pagefirstid = request.args.get('pgno')
    #pagefirstid = 0
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    d = cursor1.execute("select * from [" +value+"] order by id OFFSET "+ str(pagefirstid) +" ROWS FETCH NEXT 10 ROWS ONLY")
    print(d)
    data = cursor1.fetchall()
    mydb.close()
    if(session['usertype'] == 'Analyst'):
        return render_template('dashboard1.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value})
    elif(session['usertype'] == 'Approver' or session['usertype'] == 'Superadmin'):
        return render_template('dashboard2.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value})
    elif( session['usertype'] == 'Admin'):
        return render_template('dashboard.php',variable={'username': session['user'],'usertype': session['usertype'],'data':data,'pgid':pagefirstid,'value':value})

@app.route('/users_page')
def users_page():
    if(session['usertype'] == 'Admin' or session['usertype'] == 'Superadmin' ):
        mydb = dbconnect()
        cursor4 = mydb.cursor()
        cursor4.execute("select * from users")
        data = cursor4.fetchall()
        mydb.close()
        return render_template('users.php',variable={'username': session['user'],'usertype': session['usertype'] ,'data':data})
    else:
        return render_template('login.html')

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
        cursor1.execute("select * from [" +value['data1']+"] where article_id = ?",value['data'])
        main_data = cursor1.fetchall()
        return main_data

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

@app.route('/Scrapeit')
def Scrapeit():
    options = Options()
    #Chrome_Options is deprecated. So we use options instead.
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
    chromeDriverFilePath = os.path.join(ROOT_DIR,'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #,chrome_options=options
    driver = webdriver.Chrome(executable_path=chromeDriverFilePath)
    def Scrape(URL,heading,text,date,sid,sname,Count,webname,current_aricle_heading):
        driver.get(URL)
        time.sleep(3)
        c = 0
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
                            Heading = heading
        try:
            Text = driver.find_element_by_class_name(text).find_elements_by_tag_name('p')
            Text1 = []
            for p in Text:
                Text1.append(p.text)
                s = "."
                Text = s.join(Text1)
        except:
            try:
                ext = driver.find_elements_by_tag_name('p')
                Text1 = []
                for p in Text:
                    Text1.append(p.text)
                    s = "."
                    Text = s.join(Text1)
            except:
                Text = ''
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
                    except:Date = ''

        Result = {}
        # Result['Website'] = Website
        Result['Heading'] = Heading
        Result['Text'] = Text
        Result['Date'] = Date
        Result['URL'] = URL


        # return Result
        print(Heading)
        print(current_aricle_heading)
        print(str(Heading) == current_aricle_heading)
        if(str(Heading) == current_aricle_heading):
            print('ifff')
            return
        else:
            print('elseeee')
            c = c+1
            if c == 1:
                mydb = dbconnect()
                cursor1 = mydb.cursor()
                cursor1.execute("""update schema_mapping_data set latest_article_title=? where section_name=?""", (Heading, webname))
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
        mydb = dbconnect()
        cursor = mydb.cursor()
        # Section_id = 'Select section_id from schema_mapping_data where id = 4'
        cursor.execute("select section_id from schema_mapping_data where id =? ",webid)
        Value1 = cursor.fetchone()
        sid = Value1.section_id
        cursor.execute("Select section_name from schema_mapping_data where id =?",webid)
        Value2 = cursor.fetchone()
        sname = Value2.section_name
        mydb = dbconnect()




        cursor1 = mydb.cursor()
        print('he')
#        print("select latest_article_title from schema_mapping_data where section_name = [" +webname+"]")
        cursor1.execute("select latest_article_title from schema_mapping_data where section_name = '" +webname+"'")
        webname_point = cursor1.fetchone()
        current_aricle_heading = webname_point[0]
        print(current_aricle_heading)
        mydb.close()
        mydb = dbconnect()




        cursor1 = mydb.cursor()
        cursor1.execute("select id from [" +webname+"] order by id desc  OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY")
        webid_point = cursor1.fetchone()
        current_aricle_id = webid_point[0]
        Count = int(current_aricle_id)
        print(Count)
        mydb.close()

        myid = 0
        for i in range(start,end):
            myid = myid+logic_number
            print('My id is'+ str(myid))
            driver.get(MainURL+str(myid))
            # driver.get(str(MainURL)+str(myid))
            time.sleep(1)
            elems1 = driver.find_elements_by_class_name(urlclass)
            try:
                print('try')
                a_tag = []
                for k in elems1:
                    a_tag.append(k.find_element_by_tag_name('a'))
                    l=[]
                    for b in a_tag:
                        l.append(b.get_attribute('href'))
            except:
                print('except')
                l=[]
                for b in elems1:
                    l.append(b.get_attribute('href'))
            print(l)
            for j in l:
                Count = Count + 1
                print(Scrape(j,heading,text,date,sid,sname,Count,webname,current_aricle_heading))
        return

    def Direct(Website,MainURL,heading,text,date,urlclass,section):
        cursor = mydb.cursor()
        # Section_id = 'Select section_id from schema_mapping_data where id = 4'
        cursor.execute("select section_id from schema_mapping_data where id ='26' ")
        Value1 = cursor.fetchone()
        sid = Value1.section_id
        cursor.execute("Select section_name from schema_mapping_data where id = '26'")
        Value2 = cursor.fetchone()
        sname = Value2.section_name

        # print(Value1.section_id,Value2.section_name)
        driver.get(MainURL)
        time.sleep(3)
        elems1 = driver.find_element_by_class_name(section).find_elements_by_class_name(urlclass)
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
        # print(l)
        # print(l)
        for j in l:
            Count = Count + 1
            print(Scrape(Website,j,heading,text,date,sid,sname,Count))

    value = request.args.get('website-name')
    mydb = dbconnect()
    cursor1 = mydb.cursor()
    print(value)
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
    print(param_list[0])
    if(fname == 'Main'):
        Main(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid)
        return  {'success':True}
    elif(fname == 'Direct'):
        Direct(param_list[1],int(param_list[2]),int(param_list[3]),param_list[4],int(param_list[5]),param_list[6],param_list[7],param_list[8],param_list[9],wbname,wbid)
        print('done')
        return
    else:
        print('Continue')


#Step -7(run the app)
if __name__ == '__main__':
    app.run(debug=True)