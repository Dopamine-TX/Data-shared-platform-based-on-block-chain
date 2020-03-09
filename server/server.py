import os
import pymongo
import json
import time
import math
from gridfs import *
from bson.objectid import  ObjectId
from forms import LoginForm,RegisterForm,DataForm,AlgForm
from flask import Flask,render_template,request,jsonify,redirect,url_for,flash
from flask_wtf.csrf import CsrfProtect
from model import User
from flask_login import login_user, login_required,logout_user
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict


app = Flask(__name__)
app.secret_key = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

#connect to mongodb
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = myclient.list_database_names()
mydb = myclient["app_db"]
Data = mydb["Data"]
UserT =mydb["User"]
Alg = GridFS(mydb, collection="Alg")

if "app_db" in dblist:
	print("数据库已存在！")
else:
	mydb = myclient["app_db"]
# 判断 sites 集合是否存在
collist = mydb. list_collection_names()
if "Data" in collist:   
 	print("集合已存在！")
else:
	Data = mydb["Data"]
	
print (dblist)
print (collist)

@login_manager.user_loader
def load_user(id):
    return User.get(id)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)


@app.route('/')
def index():
	form = LoginForm()
	return render_template('index.html',form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if form.validate_on_submit():
		e_mail = request.form.get('email', None)
		password = request.form.get('password', None)
		remember_me = request.form.get('remember_me', False)
		print(e_mail)
		x=UserT.find_one({"email":e_mail})
		password_hash=x["passwd"]
		user = User(e_mail)
		if check_password_hash(password_hash, password):
			print("ok!!")
			x=login_user(user, remember=remember_me)
			print(x)
			return redirect(url_for('index'))
		else:
			return "no!!!"

	return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
	form = RegisterForm()
	loginform=LoginForm()
	if form.validate_on_submit():
		public_key = request.form.get('public_key', None)
		user_name = request.form.get('username', None)
		email = request.form.get('email', None)
		password = request.form.get('password', None)
		description = request.form.get('description', None)
		remember_me = request.form.get('remember_me', False)
		password_hash = generate_password_hash(password)
		newuser={"public_key":public_key,"name":user_name,"email":email,"passwd":password_hash,"desc":description,"credibility":100}
		x=UserT.insert_one(newuser)
		print(x)
		flash('User "%s" registered successfully! Please login.' % form.username.data)
		#login_form = LoginForm()
		return redirect(url_for('index'))

	return render_template('register.html', form=form,loginform=loginform)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/alg')
def alg():
	return render_template('alg.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/moredata')
def moredata():
	return render_template('moredata.html')

@app.route('/person')
@login_required
def person():
	dataform=DataForm()
	algform=AlgForm()
	id=current_user.id
	print(id)
	data_result = Data.find({"e-mail":id}).sort('time', pymongo.DESCENDING)
	alg_result = Alg.find({"e-mail":id}).sort('time', pymongo.DESCENDING)
	data_lis = []
	alg_lis = []
	user=UserT.find_one({"email":id})
	
	#for idx in range(5):
		#lis.append(x[idx])

	for x in data_result:
		data_lis.append(x)
			


	for x in alg_result:
		alg_lis.append(x)

	# d={"data1":x[0],"data2":x[1],"data3":x[2],"data4":x[3],"data5":x[4]}
	# print(d["data1"]["time"])
	#print(lis[0]['name'])
	#print(lis[0]['_id'])
	print("mmp!")	
	return render_template('person.html',datalis=data_lis,alglis=alg_lis,dataform=dataform,algform=algform,user=user)


@app.route('/moredata/data_details/<id>')
def data_details(id):
	loginform=LoginForm()
	ob = ObjectId(id)
	print(type(ob))
	data_result = Data.find_one({"_id":ob})
	print(data_result)
	print(id)
	#for x in data_result:
		#print(x)
	
	#print(data_result[0]['name'])
	return render_template('data_details.html',lis=data_result,form=loginform)
	

@app.route('/alg/alg_details/<id>')
def alg_details(id):
	loginform=LoginForm()
	ob = ObjectId(id)
	print(type(ob))
	data_result = Alg.find_one({"_id":ob})
	print(data_result)
	print(id)
	#for x in data_result:
		#print(x)
	
	#print(data_result[0]['name'])
	return render_template('algorithm.details.html',lis=data_result,form=loginform)


@app.route('/person/send_data', methods=['POST','OPTIONS'])
@login_required
def send_data():
	form=DataForm()
	if form.validate_on_submit():
		
		data = request.form
		print(data)
	
 	# 格式化成2016-03-20 11:45:39形式
		date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		mydata = {"e-mail":current_user.id, "name": data.get("data_name"), "detail": data.get("detail"), "beizhu":data.get("beizhu"),"time":date,"used_time":0,"request_time":0}
		x = Data.insert_one(mydata)
		print(x)
	return redirect(url_for('person'))


@app.route('/person/send_alg', methods=['POST','OPTIONS'])
@login_required
def send_alg():
	form=AlgForm()
	print("kkkkk!!!\n\n")
	if form.validate_on_submit():
		print("mmmp!!\n\n")
		data = request.form
		print(data)
		f = form.file.data
		print(f)
		print(f.filename)
		filename = secure_filename(f.filename)	
		
	#f = data.file.data
		
 	# 格式化成2016-03-20 11:45:39形式
		date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		mydata = {"e-mail":current_user.id, "algname": data.get("alg_name"), "detail": data.get("detail"), "beizhu":data.get("beizhu"),"time":date,"used_time":0,"data_form":data.get("data_form")}
		x = Alg.put(f,filename=filename,**mydata)
		print(x)
	return redirect(url_for('person'))


@app.route('/person/history')
@login_required
def history():
	id=current_user.id
	alg_result = Alg.find({"e-mail":id}).sort('time', pymongo.DESCENDING)
	alg_lis = []
	
	
	#for x in alg_result:
		#alg_lis.append(x)
	print(alg_result)
	#for x in data_result:
		#print(x)
	
	#print(data_result[0]['name'])
	return render_template('his_alg.html',lis=alg_result)
	

if __name__ == '__main__':

	app.run()
