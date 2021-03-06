from flask import Flask, render_template, g, url_for, request, Response
import requests
import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

application = Flask(__name__)
listOfVideoData = []

#Connect to the DB using an engine which is used behind the scenes by the ORM

engine.execute("USE hackertv")

#Use Declaratives to create a mapping
Base = declarative_base()

#Create a session
Session = sessionmaker(bind=engine)

session = Session()
Base.metadata.create_all(engine)

class VideoData(Base):
		__tablename__ = 'hackertv'

		id = Column(Integer, primary_key = True)
		title = Column(String(200))
		url = Column(String(500))
		time = Column(Integer)
		points = Column(Integer)
		created_at = Column(String(40))
		source = Column(String(200))
		image = Column(String(200))

		def __repr__(self):
			return "{VideoData(id = '%r', title = '%r', url = '%r', time = '%r', points = '%r', created_at = '%r', source = '%r', image = '%r')}" %(
					self.id, self.title, self.url, self.time, self.points, self.created_at, self.source, self.image)

#populate global list of video data
def populateList():
	global listOfVideoData

	for row in session.query(VideoData).all():
		listOfVideoData.append(row)

@application.route('/')
def index():
	global listOfVideoData

	if not listOfVideoData:
		populateList()
	
	return render_template("main.html",rows = listOfVideoData[0: 30], page = 1)

@application.route('/news')
def news():
	global listOfVideoData
	
	if not listOfVideoData:
		populateList()

	pageno = int(request.args.get('page'))
	displayStartRow = 30 * (pageno - 1)
	displayEndRow = pageno * 30
	videoDataToHTML = listOfVideoData[displayStartRow: displayEndRow]
	
	return render_template("main.html",rows = videoDataToHTML, page = pageno)	

@application.route('/output')
def tvml():
	global listOfVideoData
		
	rows = engine.execute("SELECT * from hackertv")	
	return json.dumps( [dict(ix) for ix in rows] )

if __name__ == '__main__':
	application.run()	

