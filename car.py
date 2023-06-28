from flask import Flask, render_template,request,redirect,session
import pymysql as db
from flask_session import Session
from flask_mail import Mail,Message

import os
f=os.path.join('static','image')
l=os.path.join('static','image')


app = Flask(__name__)
app.secret_key = 'super secret key'  

app.config['UPLOAD_FOLDER']=f
app.config['UPLOAD_FOLDER']=l

cnx=db.connect( user='root',
    password="Anish@2002",
    host='localhost',
    database='project',
    charset='utf8'
    )

@app.route('/')
def i():
    my=os.path.join(app.config['UPLOAD_FOLDER'],'gtr.jpg')
    return render_template("index.html",img=my)



@app.route('/carform')

def we():
    if 'email' in session and 'password' in session:
        email = session['email']
        password = session['password']
        myimage = os.path.join(app.config['UPLOAD_FOLDER'], 'car.jpeg')
        return render_template("carform.html", email=email, password=password, img=myimage)
    else:
        return redirect('/login')

  
@app.route('/carform',methods=['POST'])
def cardetails():
    if 'email' in session and 'password' in session:
        email=session['email']
        password=session['password']
        regno=request.form['r']
        Carmodel=request.form['c']
        Ownername=request.form['o']
        Companyname=request.form['cn']
        Kms=request.form['km']
        ownership=request.form['os']
        ownermobileno=request.form['on']
        expectedprice=request.form['ep']
        status=request.form['s']
        posteddate=request.form['d']
        
        
        #storing in dict
        car_data = {
            'regno': regno,
            'Carmodel': Carmodel,
            'Ownername': Ownername,
            'Companyname': Companyname,
            'Kms': Kms,
            'ownership': ownership,
            'ownermobileno': ownermobileno,
            'expectedprice': expectedprice,
            'status': status,
            'posteddate': posteddate,
            'email':email,
            'password':password
        }
        cursor = cnx.cursor()
        insert_query = "INSERT INTO rentalcar (regno, Carmodel, Ownername, Companyname, Kilometers, Ownership, Ownerphoneno, Expectedprice, Status, Posteddate,email,password) VALUES (%(regno)s, %(Carmodel)s, %(Ownername)s, %(Companyname)s, %(Kms)s, %(ownership)s, %(ownermobileno)s, %(expectedprice)s, %(status)s, %(posteddate)s,%(email)s,%(password)s)"
        cursor.execute(insert_query, car_data)
        cnx.commit()
        cursor.close()
        return redirect('/')
    else:
        return redirect('/login')
   
@app.route('/login')
def g():
    return  render_template("login.html")
@app.route('/login',methods=['POST'])
def logindetails():
    email=request.form['a']
    password=request.form['b']
    
    cursor=cnx.cursor()
    c={
        "email":email,
        "password":password
    }
    q="INSERT INTO register (email,password) VALUES(%(email)s,%(password)s)"
    cursor.execute(q,c)
    cnx.commit()
    cursor.close()
    
    return redirect('/sign')

@app.route('/home')
def web():
    cursor = cnx.cursor()
    query = "SELECT regno, Carmodel, Ownername, Companyname, Kilometers, Ownership, Ownerphoneno, Expectedprice, Status, Posteddate,email FROM rentalcar"
    cursor.execute(query)
    car_data = cursor.fetchall()
    cursor.close()
    car_data_dict = {}
    for row in car_data:
        regno = row[0]
        Carmodel = row[1]
        Ownername = row[2]
        Companyname = row[3]
        Kms = row[4]
        ownership = row[5]
        ownermobileno = row[6]
        expectedprice = row[7]
        status = row[8]
        posteddate = row[9]
        email=row[10]

        car_data_dict[regno] = {
            'Carmodel': Carmodel,
            'Ownername': Ownername,
            'Companyname': Companyname,
            'Kms': Kms,
            'ownership': ownership,
            'ownermobileno': ownermobileno,
            'expectedprice': expectedprice,
            'status': status,
            'posteddate': posteddate,
            'email':email
        }


    return render_template("home.html", args=car_data_dict)
@app.route("/search")
def search_form():
    return render_template("search.html")

@app.route("/search", methods=['POST'])
def search():
    
    search_option = request.form['c']
    search_query = request.form['f']

    cursor = cnx.cursor()
    query = "SELECT * FROM rentalcar WHERE {} = %s".format(search_option)
    cursor.execute(query, search_query)
    car_data = cursor.fetchall()
    cursor.close()


    return render_template("results.html",cars=car_data)
@app.route('/ch')
def gym():
    return render_template('ch.html')
@app.route('/sign')
def sign():
    return render_template("sign.html")
@app.route('/sign',methods=['POST'])
def sign_submit():
    e=request.form['ec']
    p=request.form['cs']
    cursor=cnx.cursor()
    qr="SELECT COUNT(*) from register where email=%s and password=%s"
    cursor.execute(qr,(e,p))
    result=cursor.fetchone()[0]
    
    cursor.close()
    if result==1 :
        session['email']=e
        session['password']=p
        return redirect('/ch')
    else:
        return render_template('unf.html')
# for sending Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='carsales489@gmail.com'
app.config['MAIL_PASSWORD']='lxncouhwekdxshey'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

@app.route('/buy')
def buy():
    return render_template('buy.html')
@app.route('/buy',methods=['POST'])

def buydetails():
   
    regno=request.form['jio']
    cursor=cnx.cursor()
    q="SELECT COUNT(*) FROM rentalcar where regno=%s and Status='unsold'"
    cursor.execute(q,regno)
    res=cursor.fetchone()[0]
    cursor.close()
    
    if res==1:
        cursor=cnx.cursor()

        q="UPDATE rentalcar SET Status ='sold' WHERE regno=%s"
        cursor.execute(q,regno)
        cnx.commit()
        e="SELECT email FROM rentalcar WHERE regno=%s"
        cursor.execute(e,regno)
        r=cursor.fetchone()
        if r:
            recipient_email=r[0]
            msg=Message('about mail',sender='carsales489@gmail.com',recipients=['carsales489@gmail.com',recipient_email])
            msg.body="YOU car has been soled"
            mail.send(msg)
            cursor.close()
            return "Mail sent"
        else:
            cursor.close()
            return "Email not sent"
            
    else:
        return render_template("buyfailed.html")


    
if __name__ == "__main__":
    app.run(debug=True)

    
    