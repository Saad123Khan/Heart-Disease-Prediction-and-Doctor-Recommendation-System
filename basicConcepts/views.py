from sqlite3 import SQLITE_SELECT
from django.shortcuts import render
from joblib import load
import numpy as np
import difflib
import mysql.connector as sql

usernameLogin=''
passwordLogin=''

def loginaction(request):
    global usernameLogin,passwordLogin
    if request.method=="POST":
        m=sql.connect(host="localhost",user="root",passwd="saad",database='website')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="username":
                usernameLogin=value
            if key=="password":
                passwordLogin=value
        
        c="select * from users where Username='{}' and Password='{}'".format(usernameLogin,passwordLogin)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t == (): 
            messagess = "Username Or Password Wrong!"
            return render(request,'login.html',{'login' : messagess})
        else:
            messagess = "Welcome !"
            return render(request,"main.html",{'login' : messagess})

    return render(request,'login.html')

def signaction(request):
    
    if request.method == "POST":
        
        m=sql.connect(host="localhost",user="root",passwd="saad",database='website')
        cursor=m.cursor()

        username = request.POST['username']
        gender = request.POST['gender']
        age = request.POST['age']
        email = request.POST['email']
        password = request.POST['password']
            
        c="insert into users Values('{}','{}','{}','{}','{}')".format(username,gender,age,email,password)
        cursor.execute(c)
        m.commit()
        
    return render(request,'login.html')

adminusername = ''
adminpassword = ''

def adnminlogin(request):
    global adminusername,adminpassword
    if request.method=="POST":
        m=sql.connect(host="localhost",user="root",passwd="saad",database='website')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="username":
                adminusername=value
            if key=="password":
                adminpassword=value
        
        c="select * from admin where username='{}' and password='{}'".format(adminusername,adminpassword)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t == (): 
            messagess = "Username Or Password Wrong!"
            return render(request,'loginadmin.html',{'admin' : messagess})
        else:
            messagess = "Welcome !"
            return render(request,"adminhome.html",{'admin' : messagess})

    return render(request,'loginadmin.html')


def userlist(request):
    con = sql.connect(user='root', password='saad', host='localhost', database='website')
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    userlist =cur.fetchall()
    
    con.commit()
    cur.close()
    con.close()

    return render(request, "usernamelist.html", {'userlist':userlist})


def prediction(request):
    con = sql.connect(user='root', password='saad', host='localhost', database='website')
    cur = con.cursor()
    cur.execute("SELECT * FROM Prediction")
    pred =cur.fetchall()
    
    con.commit()
    cur.close()
    con.close()

    return render(request, "prediction.html", {'pred':pred})

def message(request):
    con = sql.connect(user='root', password='saad', host='localhost', database='website')
    cur = con.cursor()
    cur.execute("SELECT * FROM contact")
    mess =cur.fetchall()

    con.commit()
    cur.close()
    con.close()

    return render(request, "message.html", {'mess':mess})


def Contactus(request):
    
    if request.method == "POST":
        
        m=sql.connect(host="localhost",user="root",passwd="saad",database='website')
        cursor=m.cursor()

        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
            
        c="insert into contact Values('{}','{}','{}','{}')".format(name,email,subject,message)
        cursor.execute(c)
        m.commit()

        
    return render(request,'contactus.html')


def login(request):
    return render(request ,'login.html')

def admin(request):
    return render(request ,'adminhome.html')

def adminmessage(request):
    return render(request ,'message.html')

def Main(request):
    return render(request ,'main.html')

def Output(request):
    return render (request,'output.html')

def About(request):
    return render (request,'about.html')


model = load('./savedModels/model.joblib')
df = load('./savedModels/df.joblib')
close_match = load('./savedModels/close_match.joblib')
finding_close_match = load('./savedModels/finding_close_match.joblib')
similarity = load('./savedModels/similarity.joblib')
similarityscore = load('./savedModels/similarityscore.joblib')
sorted_similar_location = load('./savedModels/sorted_similar_location.joblib')
list_of_all_location = load('./savedModels/list_of_all_location.joblib')
index_of_the_doctor = load('./savedModels/index_of_the_doctor.joblib')


def formInfo(request):
    
    m=sql.connect(host="localhost",user="root",passwd="saad",database='website')
    cursor=m.cursor()

    age = request.POST['age']
    sex = request.POST['sex']
    cp = request.POST['cp']
    trestbps = request.POST['trestbps']
    chol = request.POST['chol']
    fbs = request.POST['fbs']
    restecg = request.POST['restecg']
    thalach = request.POST['thalach']
    exang = request.POST['exang']
    oldpeak = request.POST['oldpeak']
    slope = request.POST['slope']
    ca = request.POST['ca']
    thal = request.POST['thal']

    input_data = (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
    inputdataasnparray = np.asarray(input_data,dtype=np.int64)
    inputdatareshaped = inputdataasnparray.reshape(1,-1)
    ypred = model.predict(inputdatareshaped)        
    
    if ypred[0] == 0:
        ypred = "Not Heart Disease"
        y = 0
    elif ypred[0] == 1:
        ypred = "Heart Disease"
        y = 1
    c="insert into Prediction Values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,y)
    cursor.execute(c)
    m.commit()  
    
    return render (request,'output.html', {'output' : ypred})


def recommendation(request): 

    Locat = request.GET['loc']
    list_of_all_location = df['Location'].tolist()
    finding_close_match = difflib.get_close_matches(Locat,list_of_all_location)
    close_match = finding_close_match[0]
    index_of_the_doctor = df[df.Location == close_match]['Index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_doctor]))
    sorted_similar_location = sorted(similarity_score , key = lambda x:x[1], reverse = True)
    

    ContactList = []


    data = []
    i = 1
    for title in sorted_similar_location:
         index = title[0]
         Name_Index = df[df.index == index]['Doctor_Name'].values[0]
         Gender_Index = df[df.index == index]['Gender'].values[0] 
         Age_Index = df[df.index == index]['Age'].values[0]
         Contact_Index = df[df.index == index]['Contact_No'].values[0] 
         Qualification_Index = df[df.index == index]['Qualification'].values[0]
         Location_Index = df[df.index == index]['Location'].values[0] 
         Image_Index = df[df.index == index]['Image'].values[0] 
         
         item = []
         if( i<=8):
             print(i,Name_Index,Gender_Index,Age_Index,Contact_Index,Qualification_Index,Location_Index,Image_Index)
             item.append(Name_Index)
             item.append(Gender_Index)
             item.append(Age_Index)
             item.append(Contact_Index)
             item.append(Qualification_Index)
             item.append(Location_Index)   
             item.append(Image_Index)
               
             ContactList.append(Contact_Index)
             data.append(item)
             i+=1
             cont = {'yp' : data , 'cn' : ContactList }
    return render (request,'output.html'  , cont)

