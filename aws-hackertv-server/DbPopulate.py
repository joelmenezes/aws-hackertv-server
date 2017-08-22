from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import requests
import os
from urlparse import urlparse, parse_qs

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joel12345'
app.config['MYSQL_DB'] = 'hackertv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/hackertv'
db = SQLAlchemy(app)
db.echo = True
db.SQLALCHEMY_TRACK_MODIFICATIONS = True

class VideoData(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(120))
	url = db.Column(db.String(120))
	time = db.Column(db.Integer)
	points = db.Column(db.Integer)
	created_at = db.Column(db.String(40))
	source = db.Column(db.String(40))
	image = db.Column(db.String(50))

	def __init__(self, id, title, url, time, points, created_at, source, image): #add image parameter
		self.id = id
		self.title = title
		self.url = url
		self.time = time
		self.points = points
		self.created_at = created_at
		self.source = source
		self.image = image

	def __repr__(self):
			return '<VideoData %r>' % self.id

def populate_db():
	print("Done")
	
	r = requests.get('http://hn.algolia.com/api/v1/search?query=[video]&tags=story&hitsPerPage=1000')
	r = r.json()
	print("GET received")
	db.create_all()
	for hit in r['hits']:

		sourceAndImage = getSourceAndImg(hit['url'])
		
		date = hit['created_at'].strip()
		date = date.split("T")

		row = VideoData(hit['objectID'], hit['title'], hit['url'], hit['created_at_i'], hit['points'], date[0], sourceAndImage['source'], sourceAndImage['imgSrc'])
		
		#Add rows to the db and commit the changes
		db.session.add(row)
		db.session.commit()
		print("Commit")
def getSourceAndImg(url):
	query = urlparse(url)

	imgSrc = ''
	source = query.netloc

	if query.hostname == 'youtu.be':
		 imgID = query.path[1:]
		 imgSrc = "http://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
	if query.hostname in ('www.youtube.com', 'youtube.com'):
		if query.path == '/watch':
		    p = parse_qs(query.query)
		    imgID = p['v'][0]
		    imgSrc = "http://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
		if query.path[:7] == '/embed/':
		    imgID = query.path.split('/')[2]
		    imgSrc = "http://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
		if query.path[:3] == '/v/':
		    imgID = query.path.split('/')[2]
		    imgSrc = "http://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
	else:
		imgSrc = "/static/defaultThumbnail.png"	    		

	return {'source':source, 'imgSrc':imgSrc}


populate_db()