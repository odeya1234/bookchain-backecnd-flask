from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import sys
import string
import random
from pathlib import Path

app = Flask('helloworld')

app_dir = Path(sys.argv[0]).resolve().parent
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app_dir}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
145

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(120), unique=False)
	lastName = db.Column(db.String(120), unique=False)
	email = db.Column(db.String(220), unique=False)
	area = db.Column(db.String(220), unique=False)
	
	def __init__(self, firstName, lastName, email, area):
		self.id = ''.join([random.choice(string.digits) for n in range(9)])
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.area = area
		
	def as_dict(self):
		return {'firstName': self.firstName,'lastName': self.lastName,'email': self.email,'area': self.area }
		
class Book(db.Model):
	id = db.Column(db.String(12), primary_key=True)
	name = db.Column(db.String(120), unique=False)
	author = db.Column(db.String(120), unique=False)
	image = db.Column(db.String(220), unique=False)
	area = db.Column(db.String(220), unique=False)
	user = db.Column(db.String(220), unique=False)
	
	def __init__(self, name, author, image, area, user):
		self.id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
		self.name = name
		self.author = author
		self.image = image
		self.area = area
		self.user = user
		
	def as_dict(self):
		return {'name': self.name,'author': self.author,'image': self.image, 'area' : self.area }
	
	
@app.route('/')
def show_all():
	return Books_as_json(Book.query.all())

#User methods		
@app.route('/users', methods=['GET'])
def index():
	return Users_as_json()

@app.route('/insert_user', methods=['GET'])
def form_user():
	return '''<form method="POST">
				  first_name: <input type="text" name="first_name"><br>
				  last_name: <input type="text" name="last_name"><br>
				  area: <input type="text" name="area"><br>
				  email: <input type="text" name="email"><br>
				  <input type="submit" value="Submit"><br>
			  </form>'''
			  
@app.route('/insert_user', methods=['POST'])
def create():
	newFirstName = request.form['first_name']
	newLastName = request.form['last_name']
	newEmail = request.form['email']
	newarea = request.form['area']
	user = User(newFirstName, newLastName, newEmail, newarea)
	db.session.add(user)
	db.session.commit()
	return Users_as_json(User.query.all())
	
@app.route('/find_person/<id>')
def findUser(id):
	user = User.query.filter_by(id=id).first()
	return Users_as_json([user])

def Users_as_json(users):
	return jsonify([m.as_dict() for m in users])

	
#Book methods
@app.route('/books', methods=['GET'])
def books():
	name = request.args.get('name')
	author = request.args.get('author')
	area = request.args.get('area')
	user = request.args.get('user')
	
	book = Book.query.all()
	if name:
		book = Book.query.filter_by(name=name)
	if author:
		book = Book.query.filter_by(author=author)	
	if area:
		book = Book.query.filter_by(area=area)	
	if user:
		book = Book.query.filter_by(user=user)
	#book = Book.query.filter(Book.name.contains(name)).all()
	return Books_as_json(book)

@app.route('/books/<id>')
def findBooks_name(name):
	book = Book.query.filter_by(id=id)
	return jsonify([m.as_dict() for m in book])

@app.route('/insert_book', methods=['GET'])
def form_example():
	return '''<form method="POST">
				  Name: <input type="text" name="name"><br>
				  Author: <input type="text" name="author"><br>
				  area: <input type="text" name="area"><br>
				  Image: <input type="text" name="image"><br>
				  <input type="submit" value="Submit"><br>
			  </form>'''
			  
@app.route('/insert_book', methods=['POST'])
def insert_book():
	newName = request.form['name']
	newAuthor = request.form['author']
	newImage = "IMG_8624.JPG" #= request.form['image']
	newarea = request.form['area']
	book = Book(newName, newAuthor, newImage, newarea, "1234")
	db.session.add(book)
	db.session.commit()
	return Books_as_json([book])
		

def Books_as_json(books):
	return jsonify([m.as_dict() for m in books])

if __name__ == '__main__':
	if len(sys.argv) == 1:
		sys.exit(f'Usage: {sys.argv[0]} <start|init>')

	if sys.argv[1] == 'init':
		db.create_all()
		sys.exit()

	if sys.argv[1] == 'start':
		app.run()
		sys.exit()