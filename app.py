from flask import Flask, request, render_template, redirect, session, url_for
from flaskext.mysql import MySQL
import time
from datetime import datetime

#from flask_mysqldb import MySQL, MySQLdb
#import bcyrypt
#import phase3

mysql = MySQL()
app = Flask(__name__)
app.secret_key = "abc"

#app.config["MYSQL_DATABASE_USER"] = "root"
#app.config["MYSQL_DATABASE_PASSWORD"] = "mlkMS1978"
#app.config["MYSQL_DATABASE_DB"] = "cs6400_fa18_team022_2"
#app.config["MYSQL_DATABASE_HOST"] = "localhost"
#step2
#app.config["MYSQL_CURSORCLASS"] = "Dictcursor"
#mysql.init_app(app)

def getMysqlConnection():

    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = "root"
    app.config['MYSQL_DATABASE_PASSWORD'] = "mlkMS1978"
    app.config['MYSQL_DATABASE_DB'] = "cs6400_fa18_team022_2"
    app.config['MYSQL_DATABASE_HOST'] = "localhost"

    mysql.init_app(app)

    connection = mysql.connect()
    cursor = connection.cursor()
    return {"cursor":cursor,"connection":connection}

db =  getMysqlConnection()
cursor = db['cursor']
connection = db['connection']


@app.route("/")
def my_form():
    # render an login.html template and pass it the data you retrieved from the database
	#cursor = db['cursor']
	#connection = db['connection']
	#message = session['message']
	session['message'] = ''
	session['emailmessage'] = ''
	session['pinmessage'] = ''
	session['collections'] = []
	session['products'] = []
	session['collection-products'] = {}
	return render_template("login.html", message=session['message'])
	
@app.route("/",methods=['POST'])
def login_validation():
	session['message'] = ''
	session['emailmessage'] = ''
	session['pinmessage'] = ''
	cursor = db['cursor']
	connection = db['connection']
	email = request.form['e']
	pin = request.form['p']
	#cursor = mysql.connect().cursor()
	cursor = db['cursor']
	cursor.execute("SELECT * FROM User WHERE email='"+email+"' and PIN='"+pin+"'")
	data = cursor.fetchone()
	cursor.execute("SELECT * FROM User WHERE email='"+email+"'")
	userdata = cursor.fetchone()
	cursor.execute("SELECT PIN FROM User WHERE email='"+email+"' and PIN='"+pin+"'")
	pindata = cursor.fetchone()
	if data is None:
		if userdata is None:
			session['emailmessage'] = "This email does not exist in our database"
		else:
			if pindata is None:
				session['pinmessage'] = "The PIN is wrong"	
			#if pindata is not None and pindata[0] != pin:
			#	session['pinmessage'] = "The PIN is wrong"
		#session['message'] = "User email or password is wrong"
		return render_template("login.html", message = session['message'], emailmessage=session['emailmessage'], pinmessage=session['pinmessage']) 
	else:
		session['email'] = email
		session['pin'] = pin
		return redirect("/activity")

@app.route("/activity",methods=['GET','POST'])
def activity():
	session['CustomerName'] = ''
	cursor = db['cursor']
	cursor.execute("SELECT first_name, last_name FROM User WHERE email='"+session['email']+"'")
	personal_info = cursor.fetchone()
	# recent corkboards
	cursor.execute("select * from collections;")
	collection_names = cursor.fetchall()
	cursor.execute("select `Product/Service Name` from product_table_ba;")
	product_names = cursor.fetchall()
	cursor.execute("select `Product/Service Name` from product_table_ba;")
	wall_names = cursor.fetchall()
	#strftimefunc = time.strftime
	#datelist = []
	#timelist = []
	#for recent in recentdata:
		#date = recent[5].strftime("%B %d,%Y")
		#datelist.append(date)
		#mytime =  recent[5].strftime("%I:%M %p")
		#timelist.append(mytime)
		
	#my-corkboards
	#cursor.execute("SELECT c.corkboardID, c.title, c.is_private, count(v.pushpinID) FROM v_pushpins v  RIGHT JOIN v_all_corkboards c ON c.corkboardID = v.corkboardID WHERE c.email='"+session['email']+"' GROUP BY 1,2,3 ORDER BY c.title")
	#data = cursor.fetchall()
	selected_collections = session['collections']
	selected_collection_products = session['collection-products']
	
	#return render_template("homepage.html",data = data, recent = recentdata, personal = personal_info, datelist = datelist, timelist = timelist, strftimefunc = strftimefunc)
	return render_template("activity.html", collections = collection_names, personal=personal_info, productnames=product_names, walls = wall_names, selected_collections=selected_collections,
	selected_collection_products = selected_collection_products)	

@app.route("/select_customer_page",methods=['GET'])
def select_customer_page():
	cursor = db['cursor']
	cursor.execute("select `CustomerName` from customers;")
	customer_names = cursor.fetchall()
	return render_template("select_customer.html", customers = customer_names)
	
@app.route("/select_customer/<cname>",methods=['GET','POST'])
def select_customer(cname):
	cursor = db['cursor']
	connection = db['connection']
	#cname = request.form['cname']
	session['CustomerName'] = cname
	username = session['email']
	cursor = db['cursor']
	now = datetime.now()
	#cursor.execute("INSERT INTO pushpin (corkboardID, url, description, updatetime) VALUES(%s,%s, %s, %s)", (int(corkid), url, description, now))
	#cursor.execute("SELECT pushpinID FROM pushpin WHERE corkboardID='"+corkid+"' AND description = '"+description+"' AND url='"+url+"' ORDER BY pushpinID DESC")
	estimatestatus = 'open'
	cursor.execute("INSERT INTO estimate_customer (username, customername, estimatetime, estimatestatus) VALUES(%s,%s, %s, %s)", (str(username), str(cname), now, str(estimatestatus)))
	connection.commit()
	return redirect(f'/homepage')
	
		
	
@app.route("/homepage",methods=['GET','POST'])
def homepage():
	cursor = db['cursor']
	#email = session['email']
	#pin = session['pin']
	#customer info
	cname = session['CustomerName']
	# user info
	cursor.execute("SELECT first_name, last_name FROM User WHERE email='"+session['email']+"'")
	personal_info = cursor.fetchone()
	# recent corkboards
	cursor.execute("select * from collections;")
	collection_names = cursor.fetchall()
	cursor.execute("select `Product/Service Name` from product_table_ba;")
	product_names = cursor.fetchall()
	cursor.execute("select `Product/Service Name` from product_table_ba;")
	wall_names = cursor.fetchall()
	#strftimefunc = time.strftime
	#datelist = []
	#timelist = []
	#for recent in recentdata:
		#date = recent[5].strftime("%B %d,%Y")
		#datelist.append(date)
		#mytime =  recent[5].strftime("%I:%M %p")
		#timelist.append(mytime)
		
	#my-corkboards
	#cursor.execute("SELECT c.corkboardID, c.title, c.is_private, count(v.pushpinID) FROM v_pushpins v  RIGHT JOIN v_all_corkboards c ON c.corkboardID = v.corkboardID WHERE c.email='"+session['email']+"' GROUP BY 1,2,3 ORDER BY c.title")
	#data = cursor.fetchall()
	selected_collections = session['collections']
	selected_collection_products = session['collection-products']
	
	#return render_template("homepage.html",data = data, recent = recentdata, personal = personal_info, datelist = datelist, timelist = timelist, strftimefunc = strftimefunc)
	return render_template("homepage.html", collections = collection_names, personal=personal_info, productnames=product_names, walls = wall_names, selected_collections=selected_collections,
	selected_collection_products = selected_collection_products, cname = cname)	

@app.route("/add_collection/<collectionname>", methods=['GET','POST'])
#eg. /add_collection/'Bristol Antique'
def add_collection(collectionname):
	cursor = db['cursor']
	connection = db['connection']
	#connection = mysql.connect()
	list = session['collections']
	
	if collectionname not in list:
		list.append(collectionname)
		session['collections'] = list
		coll_prod = session['collection-products']
		coll_prod[collectionname] = {}
		session['collection-products'] = coll_prod
		
	print(session['collections'])	
	print(session['collection-products'])	
	return redirect(f'/homepage')
	
	
@app.route("/add_product/<productid>", methods=['GET','POST'])
def add_product(productid):
	cursor = db['cursor']
	connection = db['connection']
	cursor.execute("SELECT * FROM product_table_ba WHERE `Product/Service Name`='"+productid+"'")
	product_info = cursor.fetchone()
	collectionid = product_info[1]
	prodid = product_info[2]
	desc = product_info[3]
	price = product_info[5]
	cursor.execute("SELECT Collection_Name FROM collections WHERE collection='"+collectionid+"'")
	collection = cursor.fetchone()[0]
	
	selected_coll_prod_dict = session['collection-products'][collection]
	coll_prods = session['collection-products']
	if productid not in selected_coll_prod_dict:
		qty = 1
		sub = qty * price
		prod_info = [prodid,desc,price,qty, sub]
		#selected_coll_prod_list.append(productid)
		selected_coll_prod_dict[productid] = prod_info
		coll_prods[collection] = selected_coll_prod_dict
		session['collection-products'] = coll_prods
		
	else:
		qty = selected_coll_prod_dict[productid][3] + 1 
		sub = qty * price
		prod_info = [prodid,desc,price,qty, sub]
		selected_coll_prod_dict[productid] = prod_info
		coll_prods[collection] = selected_coll_prod_dict
		session['collection-products'] = coll_prods
		
	
		
	print(session['collection-products'][collection])
	return redirect(f'/homepage')

































	
@app.route("/add_cork", methods=["GET"])
def add_cork_view():
	# populate category
	cursor = db['cursor']
	cursor.execute("SELECT * FROM category_setup")
	categories = cursor.fetchall()
	return render_template("add_cork.html", categories = categories)
	
@app.route("/add_cork", methods=["POST"])
def add_cork():
	title = request.form['t']
	category = request.form['c']
	visibility = request.form['v']
	if visibility == 'private':
		password = request.form['p']
	cursor = db['cursor']
	connection = db['connection']
	
	cursor.execute("INSERT INTO corkboard (category, email, title)VALUES(%s,%s, %s)", (category, session['email'], title))
	
	if visibility == 'public':
		cursor = db['cursor']
		connection = db['connection']
		cursor.execute("SELECT corkboardID FROM corkboard WHERE title='"+title+"' AND email = '"+session['email']+"' AND category='"+category+"' ORDER BY corkboardID DESC")
		corkID = cursor.fetchone()
		corkID = corkID[0]
		cursor.execute("INSERT INTO public_corkboard VALUES(%s)", (corkID))
		connection.commit()
	else:
		cursor = db['cursor']
		connection = db['connection']
		cursor.execute("SELECT corkboardID FROM corkboard WHERE title='"+title+"' AND email = '"+session['email']+"' AND category='"+category+"' ORDER BY corkboardID DESC")
		corkID = cursor.fetchone()
		corkID = corkID[0]
		cursor.execute("INSERT INTO private_corkboard VALUES(%s,%s)", (corkID, password))
		connection.commit()
	
	return redirect(f'/view_corkboard/{corkID}')

@app.route("/view_corkboard/<corkid>", methods=["GET","POST"])
def view_corkboard(corkid):
	cursor = db['cursor']
	session['pin_add_error'] = False
	session['pin_add_error_message'] = []
	# check if the address written asks for private _corkboard
	cursor.execute("SELECT is_private FROM v_all_corkboards WHERE corkboardID = '"+corkid+"'")
	session['corkboardID'] = corkid
	cursor.execute("SELECT * FROM corkboard WHERE corkboardID='"+session['corkboardID']+"'")
	corkdata = cursor.fetchone()
	session['cemail'] = corkdata[2]
	corkowner = corkdata[2]
	session['cork_title'] = corkdata[3]
	cursor.execute("SELECT * FROM user WHERE email='"+session['cemail']+"'")
	ownerdata = cursor.fetchone()
	cursor.execute("SELECT count(*) FROM watch WHERE corkboardID='"+corkid+"'")
	watchercount = cursor.fetchone()
	cursor.execute("SELECT * FROM pushpin WHERE corkboardID='"+session['corkboardID']+"'")
	pindata = cursor.fetchall()
	cursor.execute("SELECT max(updatetime) FROM pushpin WHERE corkboardID='"+session['corkboardID']+"'")
	update = cursor.fetchone()
	cursor.execute("SELECT * FROM private_corkboard WHERE corkboardID='"+corkid+"'")
	privatenum = cursor.fetchone()
	if session['email'] == session['cemail']:
		add_pin_b = True
	else:
		add_pin_b = False
		
	if privatenum is not None:
		display_watch_button = False
	elif (session['email'] == session['cemail']):
		display_watch_button = False
	elif (watchercount[0] > 0) and (session['email'] != session['cemail']) :
		cursor.execute("SELECT wemail FROM watch WHERE corkboardID='"+corkid+"'")
		watcherlist = cursor.fetchall()
		for watcher in watcherlist:
			if (session['email'] == watcher[0]):
				display_watch_button = False
				break
			else:
				display_watch_button = True
	else:
		display_watch_button = True
		
	if privatenum is not None:
		private = True
	else:
		private = False
	if watchercount[0]>0:
		cursor.execute("SELECT wemail FROM watch WHERE corkboardID='"+corkid+"'")
		watcherlist = cursor.fetchall()
	if (watchercount[0] == 0) or (watchercount is None):
		watcherlist = []
		
	cursor.execute("SELECT femail FROM follow WHERE email='"+session['cemail']+"'")
	followeremails = cursor.fetchall()
	
	if (corkowner == session['email']):
		display_f_b = False
	elif (len(followeremails) > 0):
		for follower in followeremails:
			if (session['email'] in follower[0]):
				display_f_b = False
				break
			else:
				display_f_b = True
	else:
		display_f_b = True
	if update[0] is not None:	
		date = update[0].strftime("%B %d,%Y")
		time =  update[0].strftime("%I:%M %p")
		updatelist = [date,time]
	else:
		updatelist = []
	
	return render_template("view_corkboard.html", corkdata = corkdata, ownerdata = ownerdata, watchercount = watchercount[0], add_pin_b = add_pin_b,\
	pindata = pindata, display_w_b = display_watch_button, update = updatelist, private = private, display_f_b=display_f_b,)
	# bilgi check etmek icin eklenebilecekler : owner = session['email'], corkemail = session['cemail'], watcherlist=watcherlist

	

	
@app.route("/watch/<corkid>", methods=['POST'])
def watch(corkid):
	cursor = db['cursor']
	connection = db['connection']
	#connection = mysql.connect()
	cursor.execute("INSERT INTO watch VALUES(%s,%s)", (int(corkid), session['email']))
	connection.commit()
	#addr = "pushpin/"+str(session['pushpinID'])
	return redirect(f'/view_corkboard/{corkid}')
	

@app.route("/add_pin", methods=['GET'])
def get_add_pin():
	cursor = db['cursor']
	connection = db['connection']
	corktitle = session['cork_title']
	if session['pin_add_error']:
		message = session['pin_add_error_message']
	else:
		message = []
	return render_template('add_pin.html', corktitle = corktitle, message = message)

	
@app.route("/add_pin", methods=['POST'])
def add_pin():
	cursor = db['cursor']
	connection = db['connection']
	url = request.form['u']
	description = request.form['d']
	tags = request.form['t']
	urlmessage = ''
	tagmessage = ''
	imgerror = False
	tagerror = False
	urllengtherror = False
	# check image style
	img_list = ['.jpg','.png','.gif','.jpeg']
	for type in img_list:
		if url.find(type) != -1:
			urlmessage =''
			img_type_found = True
			imgerror = False
			break
		else:
			imgerror = True
			urlmessage = "Img type not supported Images should be one of the :.jpg, .jpeg, .png or .gif types "
	# check the lengths of tags
	taglist = tags.split(',')
	for tag in taglist:
		if len(tag) > 20:
			tagmessage = "Tag maximum length exceeded. Each Tag should be shorter than 20 characters."
			tagerror = True
			break
		else:
			tagmessage = ''
	# check url length
	if len(url) > 200:
		urllengthmessage = "Url longer than 200 characters"
		urllengtherror = True
	else:
		urllengthmessage = ''
		urllengtherror = False
	message = [urlmessage, tagmessage, urllengthmessage]
	if imgerror or tagerror or urllengtherror:
		session['pin_add_error'] = True
		session['pin_add_error_message'] = message
		return redirect('/add_pin')
	else:
		session['pin_add_error'] = False
		session['pin_add_error_message'] = []
	
	corkid = session['corkboardID']
	now = datetime.now()
	cursor.execute("INSERT INTO pushpin (corkboardID, url, description, updatetime) VALUES(%s,%s, %s, %s)", (int(corkid), url, description, now))
	cursor.execute("SELECT pushpinID FROM pushpin WHERE corkboardID='"+corkid+"' AND description = '"+description+"' AND url='"+url+"' ORDER BY pushpinID DESC")
	pinid = cursor.fetchone()[0]
	taglist = tags.split(',')
	for tag in taglist:
		cursor.execute("INSERT INTO pushpintag VALUES(%s,%s)", (int(pinid), tag))
	connection.commit()
	return redirect(f'/view_corkboard/{corkid}')
	

@app.route("/pushpin/<pinid>", methods=["GET","POST"])
def pushpin(pinid):
	if request.method == "GET":
		#cursor = mysql.connect().cursor()
		cursor = db['cursor']
		session['pushpinID'] = pinid
		cursor.execute("SELECT *,SUBSTRING_INDEX(SUBSTRING_INDEX(url,'//',-1),'/',1) as Site FROM pushpin WHERE pushpinID='"+session['pushpinID']+"'")
		pindata = cursor.fetchone()
		session['corkboardID'] = str(pindata[1])
		cursor.execute("SELECT first_name, last_name, user.email, title, corkboardID FROM user JOIN corkboard ON user.email = corkboard.email WHERE corkboardID='"+session['corkboardID']+"'")
		ownerdata = cursor.fetchone()
		pinowner = ownerdata[2]
		session['pinemail'] = pinowner
		cursor.execute("SELECT tag FROM pushpintag WHERE pushpinID='"+session['pushpinID']+"'")
		tagdata = cursor.fetchall()
		cursor.execute("SELECT first_name, last_name, user.email FROM like_unlike JOIN user ON lemail = email WHERE pushpinID='"+session['pushpinID']+"'")
		likers = cursor.fetchall()
		cursor.execute("SELECT lemail FROM like_unlike WHERE pushpinID='"+session['pushpinID']+"'")
		likeremails = cursor.fetchall()
		cursor.execute("SELECT femail FROM follow WHERE email='"+session['pinemail']+"'")
		followeremails = cursor.fetchall()
		cursor.execute("SELECT first_name, last_name, user.email, ucomment FROM comment JOIN user ON comment.cemail = user.email WHERE pushpinID='"+session['pushpinID']+"' ORDER BY commentdatetime DESC")
		comments = cursor.fetchall()
		if (pinowner == session['email']):
			display_f_b = False
		elif (len(followeremails) > 0):
			for follower in followeremails:
				if (session['email'] in follower[0]):
					display_f_b = False
					break
				else:
					display_f_b = True
		else:
			display_f_b = True
			
		if session['email'] == pinowner:
			display_lu_b = False
		else:
			display_lu_b = True
			
		if len(likeremails)>0 :	
			for liker in likeremails:
				if (session['email'] in liker[0]):
					#if the user is in likers list, don't display like button, display unlike button
					display_like = False
					break
				else:
					display_like = True
		else:
			display_like = True
		button = [display_f_b, display_like, display_lu_b]
		
		date = pindata[4].strftime("%B %d,%Y")
		time =  pindata[4].strftime("%I:%M %p")
		datetime = [date,time]
		return render_template("pushpin.html", pindata = pindata, ownerdata = ownerdata, tagdata = tagdata, likers = likers, comments = comments, button=button, datetime=datetime)


@app.route("/follow", methods=["POST"])
def follow():
	cursor = db['cursor']
	connection = db['connection']
	pinid = session['pushpinID']
	cursor.execute("INSERT INTO follow VALUES(%s,%s)", (session['pinemail'], session['email']))
	connection.commit()
	#addr = "pushpin/"+str(session['pushpinID'])
	return redirect(f'/pushpin/{pinid}')
		
@app.route("/comment", methods=["POST"])
def comment():
	newcomment = request.form['comment']
	#cursor = mysql.connect().cursor()
	cursor = db['cursor']
	connection = db['connection']
	pinid = session['pushpinID']
	#connection = mysql.connect()
	if newcomment != "":
		now = datetime.now()
		cursor.execute("INSERT INTO comment VALUES(%s,%s, %s, %s)", (int(session['pushpinID']), session['email'], now, newcomment))
		connection.commit()
	#addr = "pushpin/"+str(session['pushpinID'])
	return redirect(f'/pushpin/{pinid}')
	
@app.route("/like/<pinid>", methods=['POST'])
def like(pinid):
	cursor = db['cursor']
	connection = db['connection']
	#connection = mysql.connect()
	cursor.execute("INSERT INTO like_unlike VALUES(%s,%s)", (int(pinid), session['email']))
	connection.commit()
	#addr = "pushpin/"+str(session['pushpinID'])
	return redirect(f'/pushpin/{pinid}')
	
@app.route("/unlike/<pinid>", methods=['POST'])
def unlike(pinid):
	cursor = db['cursor']
	connection = db['connection']
	#connection = mysql.connect()
	cursor.execute("DELETE FROM like_unlike WHERE pushpinID='"+session['pushpinID']+"' AND lemail='"+session['email']+"'")
	connection.commit()
	#addr = "pushpin/"+str(session['pushpinID'])
	return redirect(f'/pushpin/{pinid}')
		
@app.route("/popular_tags", methods=["GET"])
def popular_tags():
	# populate category
	cursor = db['cursor']
	cursor.execute("SELECT * FROM v_popular_tags")
	populardata = cursor.fetchall()
	return render_template("popular_tags.html", populardata=populardata)

@app.route("/search_popular_tags/<tag>", methods=["GET"])
def search_popular_tags(tag):
	# populate category
	cursor = db['cursor']
	#cursor.execute("select p.pushpinID, p.description, pt.tag, c.category, c.title, u.first_name ,u.last_name \
	#from user u join v_all_corkboards c on u.email = c.email join pushpin p \
	#on c.corkboardID = p.corkboardID join pushpintag pt on p.pushpinID = pt.pushpinID where is_private = 0")
	cursor.execute("SELECT distinct email,PushPin_Description,CorkBoard_Title,owner, pushpinID \
	FROM V_PUSHPIN_SEARCH \
	WHERE ((lower(pushpin_tags) like '%"+tag+"%') OR (lower(PushPin_Description) like '%"+tag+"%') OR (lower(category) like '%"+tag+"%')) and is_private=0")
	searchdata = cursor.fetchall()
	searchdatanew = []
	searchlist = []
	#for search in searchdata:
	#	if tag in search[1]:
	#		if search[1] not in searchlist:
	#			searchlist.append(search[1])
	#			searchdatanew.append(search)
	#		if search[1] not in searchlist:
	#			searchlist.append(search[1])
	#			searchdatanew.append(search)
	#	if tag in search[3]:
	#		if search[1] not in searchlist:
	#			searchlist.append(search[1])
	#			searchdatanew.append(search)
	return render_template("search_tag_results.html", searchdata=searchdata)

@app.route("/search", methods=["POST"])
def search():
	# populate category
	cursor = db['cursor']
	key = request.form['s']
	cursor.execute("SELECT distinct email,PushPin_Description,CorkBoard_Title,owner, pushpinID \
	FROM V_PUSHPIN_SEARCH \
	WHERE ((lower(pushpin_tags) like '%"+key+"%') OR (lower(PushPin_Description) like '%"+key+"%') OR (lower(category) like '%"+key+"%')) and is_private=0")
	searchdata = cursor.fetchall()
	searchdatanew = []
	searchlist = []

	return render_template("search_results.html", searchdata=searchdata)	

@app.route("/popular_sites", methods=["GET"])
def popular_sites():
	# populate category
	cursor = db['cursor']
	cursor.execute("SELECT * FROM v_popular_sites")
	searchdata = cursor.fetchall()
	return render_template("popular_sites.html", searchdata=searchdata)
	
@app.route("/corkboard_statistics", methods=["GET"])
def corkboard_statistics():
	# populate category
	cursor = db['cursor']
	cursor.execute("SELECT * FROM v_corkboard_statistics")
	useremail = session['email']
	statistics = cursor.fetchall()
	return render_template("corkboard_statistics.html", statistics=statistics, useremail=useremail)

@app.route("/askpassword/<corkID>",methods=['GET'])
def ask_password(corkID):
	return render_template("askpassword.html", corkID = corkID)
	
@app.route("/askpassword/<corkID>",methods=['POST'])
def password_validation(corkID):
	cursor = db['cursor']
	connection = db['connection']
	password = request.form['pass']
	cursor.execute("SELECT * FROM private_corkboard WHERE corkboardID='"+corkID+"' and password='"+password+"'")
	privatedata = cursor.fetchone()
	if privatedata is None:
		message = "Password is wrong"
		return render_template("askpassword.html", corkID=corkID, message=message) 
	else:
		session['corkboardID'] = corkID
		session['password'] = password
		return redirect(f'/view_corkboard/{corkID}')
		
@app.route("/logout")
def logout():
	session.pop('email', None)
	# return render_template("login.html")		
	return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)