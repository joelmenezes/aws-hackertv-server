from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from urlparse import urlparse, parse_qs
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

#Connect to the DB using an engine which is used behind the scenes by the ORM
#add ', echo=True' for console log
engine = create_engine('mysql://hackertv:hackertvforaws@hackertv-server.cjk7sbsmwyfs.us-east-1.rds.amazonaws.com:3306/hackertvdb?charset=utf8', echo=True)
engine.execute('SET NAMES utf8;')
engine.execute('SET CHARACTER SET utf8;')
engine.execute('SET character_set_connection=utf8;')
engine.execute("SET CHARACTER SET utf8")
#engine.execute("CREATE DATABASE IF NOT EXISTS hackertv") #create db
#engine.execute("USE hackertv")
engine.execute("DROP TABLE IF EXISTS hackertv")


#Use Declaratives to create a mapping
Base = declarative_base()

#Create a session
Session = sessionmaker(bind=engine)

class VideoData(Base):
		__tablename__ = 'hackertv'

		id = Column(Integer, primary_key = True)
		title = Column(String(200))
		url = Column(String(500))
		time = Column(Integer)
		points = Column(Integer)
		created_at = Column(String(40))
		source = Column(String(200))
		image = Column(String(200)
)
		def __repr__(self):
			return "<VideoData(id = '%r', title = '%r', url = '%r', time = '%r', points = '%r', created_at = '%r', source = '%r', image = '%r')>" %(
					self.id, self.title, self.url, self.time, self.points, self.created_at, self.source, self.image)

#Populate Database with results of GET request
def populate_db():
	session = Session()
	Base.metadata.create_all(engine)

	r = requests.get('http://hn.algolia.com/api/v1/search?query=[video]&tags=story&hitsPerPage=2000')
	r = r.json()
	print("GET received")
	for hit in r['hits']:

		sourceAndImage = getSourceAndImg(hit['url'])
		
		date = hit['created_at'].strip()
		date = date.split("T")

		row = VideoData(title = hit['title'].decode('utf-8', 'ignore'), url = hit['url'].decode('utf-8', 'ignore'), time = hit['created_at_i'], points = hit['points'], created_at = date[0].decode('utf-8', 'ignore'), source = sourceAndImage['source'].decode('utf-8', 'ignore'), image = sourceAndImage['imgSrc'].decode('utf-8', 'ignore'))
		session.add(row)
		session.commit()

	try:
		session.commit()
	except:
		session.rollback()


def getSourceAndImg(url):
	query = urlparse(url)

	imgSrc = ''
	source = query.netloc

	if query.hostname == 'youtu.be':
		 imgID = query.path[1:]
		 imgSrc = "https://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
	if query.hostname in ('www.youtube.com', 'youtube.com'):
		if query.path == '/watch':
		    p = parse_qs(query.query)
		    imgID = p['v'][0]
		    imgSrc = "https://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
		if query.path[:7] == '/embed/':
		    imgID = query.path.split('/')[2]
		    imgSrc = "https://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
		if query.path[:3] == '/v/':
		    imgID = query.path.split('/')[2]
		    imgSrc = "https://img.youtube.com/vi/"+imgID+"/maxresdefault.jpg"
	else:
		imgSrc = "https://www.hackertv.io/static/defaultThumbnail.png"	    		

	return {'source':source, 'imgSrc':imgSrc}

populate_db()