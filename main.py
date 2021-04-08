import datetime;
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from sqlalchemy import text,DateTime
from functools import wraps
import random
import pickle
import numpy as np

#initialize Flask App
app=Flask(__name__)
app.secret_key = "super secret key"

#set Enviroment
ENV="dev"

#developement Environment
if ENV=="dev":
    app.debug=True
    #Local DataBase URL
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:vips@localhost:3201/cfd"
#production Environment
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#initialize Database
db=SQLAlchemy(app)

# Fraud prediction function
def ValuePredictor(to_predict_list):
    model = pickle.load(open('cfd_model.pkl', 'rb'))
    to_predict = np.array(to_predict_list).reshape(1, 11)
    result = model.predict(to_predict)
    return result[0]


#Class For users Model
class Users(db.Model):
    __tablename__="users"
    uid=db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phoneno = db.Column(db.String(200),unique=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), unique=True)

    #constructor
    def __init__(self, first_name,last_name,email,phoneno,username,password):
        self.first_name=first_name
        self.last_name=last_name
        self.phoneno=phoneno
        self.email=email
        self.username=username
        self.password=password

#Class For userAddress Model
class UserAddress(db.Model):
    __tablename__="userAddress"
    uaid=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text())
    country = db.Column(db.String(200))
    state = db.Column(db.String(200))
    district = db.Column(db.String(200))
    pincode = db.Column(db.String(200))

    def __init__(self, uid,address,country,state,district,pincode):
        self.uid=uid
        self.address=address
        self.country=country
        self.state=state
        self.district=district
        self.pincode=pincode

#Class For userCard Model
class UserCard(db.Model):
    __tablename__="userCard"
    usid=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer, nullable=False)
    name_on_card = db.Column(db.String(200))
    card_no = db.Column(db.String(200))
    expiration_date = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    bank= db.Column(db.String(200))

    def __init__(self, uid,name_on_card,card_no,expiration_date,cvv,bank):
        self.uid=uid
        self.name_on_card=name_on_card
        self.card_no=card_no
        self.expiration_date=expiration_date
        self.cvv=cvv
        self.bank=bank

#Class For transaction Model
class Transaction(db.Model):
    __tablename__="transaction"
    tid=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer, nullable=False)
    payment_type = db.Column(db.String(200))
    amount = db.Column(db.String(200))
    time = db.Column(DateTime, default=datetime.datetime.utcnow)
    platform= db.Column(db.String(200))

    def __init__(self, uid,payment_type,amount,time,platform):
        self.uid=uid
        self.payment_type=payment_type
        self.amount=amount
        self.time=time
        self.platform=platform

#Intial Route
@app.route("/")
def index():
    return render_template('index1.html')

@app.route("/signup")
def signup():
    if 'logged_in' in session:
        return render_template('product.html')
    return render_template('signup.html')

@app.route("/login")
def login():
    if 'logged_in' in session:
        return render_template('product.html')
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'logged_in' in session:

        # All the data fetched from DB
        userdata=Users.query.all()
        userAddress=UserAddress.query.all()
        userCard=UserCard.query.all()
        transaction=Transaction.query.all()

        return render_template('dashboard.html',userdata=userdata,userAddress=userAddress,userCard=userCard,transaction=transaction)
    return redirect(url_for("login"))

@app.route("/product")
def product():
    if 'logged_in' in session:
        return render_template('product.html')
    return redirect(url_for("login"))

@app.route("/checkout")
def checkout():
    if 'logged_in' in session:
        return render_template('checkout.html')
    return redirect(url_for("login"))

@app.route("/successful-payment")
def success():
    if 'logged_in' in session:
        return render_template('success.html')
    return redirect(url_for("login"))

@app.route("/fraudulent-transaction")
def fraud():
    if 'logged_in' in session:
        return render_template('PaymentError.html')
    return redirect(url_for("login"))

#function for Signup Process
@app.route("/signupSubmit",methods=['POST'])
def signupSubmit():
    if request.method == 'POST':
        #get all attributes from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phoneno = request.form['phoneno']
        username = request.form['username']
        #hash the password
        password = sha256_crypt.encrypt(str(request.form['password']))

        #data validation
        print(first_name,last_name, email,phoneno, username, password)
        if first_name == "" or last_name == "" or email=="" or phoneno=="" or username == "" or password == "":
            return render_template("register.html", message='Please enter all fields')

        #insert data to database
        if db.session.query(Users).filter(Users.first_name == first_name).count() == 0:
            data = Users(first_name,last_name, email,phoneno,username, password)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template('signup.html', message="you have already submit a form for signup!")

#function for Login Process
@app.route("/loginSubmit",methods=['POST'])
def submitLogin():
    if request.method=='POST':
        #get the data from form
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)

        if(username=="admin" and password=="admin"):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("dashboard", username=username))

        else:
            # get username & password from DB
            user_query = '''SELECT username FROM users WHERE username = :username'''
            pass_query = '''SELECT password FROM users WHERE username = :username'''
            uid_query = '''SELECT uid FROM users WHERE username = :username'''
            usernamedata = db.engine.execute(text(user_query), username=username).fetchone()
            passworddata = db.engine.execute(text(pass_query), username=username).fetchone()
            uid = db.engine.execute(text(uid_query), username=username).fetchone()
            print(usernamedata, passworddata, uid)

            # if username is not exist
            if usernamedata == None:
                return render_template('login.html')
            else:
                # if user found check the encrypted password
                for passwor_data in passworddata:
                    if sha256_crypt.verify(password, passwor_data):
                        print(passwor_data)
                        # Passed
                        session['logged_in'] = True
                        session['username'] = username

                        # redirect user to product page if logged in
                        return redirect(url_for("product", username=username))

                    else:
                        return render_template('login.html')
    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            message='Unauthorized, Please login'
            return redirect(url_for('login',message=message))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    message="You are now logged out"
    return redirect(url_for('login',message=message))



@app.route('/payment',methods=['POST'])
def payment():
    if request.method == 'POST':

        #get uid and username from db and check it
        username = request.form['username']
        session_username = session.get('username')
        user_query = '''SELECT username FROM users WHERE username = :username'''
        uid_query = '''SELECT uid FROM users WHERE username = :username'''
        usernamedata = db.engine.execute(text(user_query), username=username).fetchone()
        uid = db.engine.execute(text(uid_query), username=username).fetchone()
        userid=int(''.join(map(str, uid)))
        if usernamedata=="":
            return redirect(url_for('checkout'))

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        phoneno = request.form['phoneno']
        address = request.form['address']
        district = request.form['district']
        country = request.form['country']
        state = request.form['state']
        pincode = request.form['pincode']
        name_on_card = request.form['name_on_card']
        card_no = request.form['card_no']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']
        bank = request.form['bank']

        current_time=datetime.datetime.now()

        #insert data into various tables
        if db.session.query(UserAddress).filter(UserAddress.address == address or uid!='').count() == 0:
            data = UserAddress(int(userid),address,country,state,district,pincode)
            db.session.add(data)
            db.session.commit()

        if db.session.query(UserCard).filter(UserCard.name_on_card == name_on_card or uid!='').count() == 0:
            data = UserCard(int(userid), name_on_card, card_no, expiration_date, cvv, bank)
            db.session.add(data)
            db.session.commit()

        if db.session.query(Transaction).filter(uid!='').count() == 0:
            data = Transaction(int(userid),"online-payment","1499$",current_time,"ecommerce-website" )
            db.session.add(data)
            db.session.commit()

        #hash string values to float
        random.seed(hash(request.form['name_on_card']))
        name=random.uniform(-15.0,-10.0)

        random.seed(hash(request.form['phoneno']))
        phone = random.uniform(-2.0, 2.0)

        random.seed(hash(23.0225))
        lat=random.uniform(-2.0, 2.0)

        random.seed(hash(72.5714))
        long=random.uniform(-2.0, 2.0)

        random.seed(hash(request.form['gender']))
        gen = random.uniform(-2.0, 2.0)

        random.seed(hash(random.randint(1, 1000)))
        tid= random.uniform(-2.0, 2.0)

        random.seed(hash("Ecommerce website"))
        platform = random.uniform(-2.0, 2.0)

        random.seed(hash(datetime.datetime.utcnow))
        time = random.uniform(-2.0, 2.0)

        random.seed(hash(1499))
        transaction_amount = random.uniform(-2.0, 2.0)

        random.seed(hash(request.form['bank']))
        bankname = random.uniform(-2.0, 2.0)

        random.seed(hash("online payment"))
        reason = random.uniform(-2.0, 2.0)

        print(uid,name,phone,gen,lat,long,bankname,tid,platform,time,transaction_amount,reason)

        #pass all the features to prediction function and get result
        to_predict_list = [name,phone,gen,lat,long,bankname,tid,platform,time,transaction_amount,reason]
        result = ValuePredictor(to_predict_list)
        print(result)


    if int(result) == 1:
        prediction = 'Given transaction is  fradulent'
        return redirect(url_for('fraud'))

    else:
        prediction = 'Given transaction is not fradulent'
        return redirect(url_for('success'))

    return render_template("checkout.html",message="something went wrong")

if __name__=='__main__':
    app.debug=True
    app.run()
