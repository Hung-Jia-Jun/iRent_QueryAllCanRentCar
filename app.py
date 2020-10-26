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

queryStationList = queryStationList()
startQuery = startQuery()
@app.route("/")
def index():
	
	return render_template('map.html')

#取得用戶輸入的網址
@app.route("/getHasCarStation")
def getHasCarStation():
	startDate = request.args.get('startDate').replace("-","")
	startTime = request.args.get('startTime').replace(":","")+"00"
	endDate = request.args.get('endDate').replace("-","")
	endTime = request.args.get('endTime').replace(":","")+"00"
	
	startTime = startDate + startTime
	endTime = endDate + endTime
	carType = request.args.get('carType')
	# startTime = "20201028200000"
	# endTime = "20201028220000"
	#carType:
	#002084:SIENTA5人
	#002087:SIENTA7人
	#002669:VIOS
	#001601:YARIS
	#yyyyyy:YARIS
	#002659:PRIUSc
	# carType = "001601"
	#取得我寫在code裡面的車輛ID等資料，並去做查詢
	hasCarStation = queryStationList.start(
					startQuery, startTime, endTime, carType)
	stationJson = {}
	stationJson["hasCar"] = hasCarStation
	res_json = json.dumps(stationJson, ensure_ascii=False)
	return Response(response=res_json,
			status=200,
			mimetype="application/json")

if __name__ == "__main__":
	#為何使用8000 port呢?
	#因為小於1024的port需要sudo 才能運行
	#heroku沒有sudo 的執行權限
	#https://stackoverflow.com/questions/45385384/how-can-i-run-as-root-on-heroku
	app.run(host='0.0.0.0',port=8000)
