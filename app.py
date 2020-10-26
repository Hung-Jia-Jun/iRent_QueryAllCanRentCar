from flask import Flask,request,redirect
from flask import render_template,Response
import time
import re
import sys
from BookingCar import startQuery
from QueryCar import queryStationList
import os
import json
from flask_sqlalchemy import SQLAlchemy
import threading
import datetime
import os
from flask_migrate import Migrate
from flask_cors import cross_origin,CORS
import string
import random
import requests
from bs4 import BeautifulSoup
#------------------------------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class shortURL(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	URL = db.Column(db.String(255))
	MappingURL = db.Column(db.String(255))
  
	def __init__(self,URL,MappingURL):
		self.URL = URL
		self.MappingURL = MappingURL


queryStationList = queryStationList()
startQuery = startQuery()
@app.route("/")
def index():
	#取得我寫在code裡面的車輛ID等資料，並去做查詢
	queryStationList.start(startQuery)
	return render_template('map.html',stations = stations)

#取得用戶輸入的網址
@app.route("/getHasCarStation")
def getHasCarStation():
	# _url = request.args.get('url')
	
	res_json = json.dumps(res, ensure_ascii=False)
	return Response(response=res_json,
			status=200,
			mimetype="application/json")

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8000)
