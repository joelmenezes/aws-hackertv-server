from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from urlparse import urlparse, parse_qs
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

#Connect to the DB using an engine which is used behind the scenes by the ORM
engine = create_engine('mysql://hackertv:hackertvforaws@hackertv-server.cjk7sbsmwyfs.us-east-1.rds.amazonaws.com:3306/hackertv?charset=utf8', echo=True)
engine.execute('SET NAMES utf8;')
engine.execute('SET CHARACTER SET utf8;')
engine.execute('SET character_set_connection=utf8;')
engine.execute("SET CHARACTER SET utf8")
engine.execute("DROP TABLE hackertv")
engine.execute("DROP DATABASE IF EXISTS hackertv") #create db
#engine.execute("USE hackertv")
