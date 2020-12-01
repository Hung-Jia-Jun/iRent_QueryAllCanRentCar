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
from flask_socketio import SocketIO, emit
from bs4 import BeautifulSoup
#------------------------------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
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
	cityName = request.args.get('cityName')
	
	#取得我寫在code裡面的車輛ID等資料，並去做查詢
	hasCarStation = queryStationList.start(
            startQuery, startTime, endTime, carType, cityName)
	stationJson = {}
	
	#使用yield模式一次取出一筆目前進度，實現進度條
	stationLen , hascar  = next(hasCarStation)
	for i in range(stationLen-1):
		# 不要一次查太多
		# 所有車站都爬完很耗時間
		if len(hascar)>=10:
			continue
		stationLen , hascar = next(hasCarStation)
		#發送訊息給前端r
		socketio.emit('server_response', 
						{ 'data': {"status":str(i)+"/"+str(stationLen)+"/"+str(len(hascar))},
						'msg':"共"+str(stationLen)+"個站點，正在查詢第"+str(i)+"個站點，目前有車的站點數量："+str(len(hascar)) })
	stationJson["hasCar"] = hascar
	res_json = json.dumps(stationJson, ensure_ascii=False)
	return Response(response=res_json,
			status=200,
			mimetype="application/json")


@socketio.on('Client_event')
@cross_origin()
#接收來自前端的訊息
def Client_event(msg):
	print(msg["data"])
	# socketio.emit('server_response', { 'data': str("OK", encoding = "utf-8") })
	#發送訊息給前端
	socketio.emit('server_response', { 'data': "OK" })
	return Response(status=200)

if __name__ == "__main__":
	#為何使用8000 port呢?
	#因為小於1024的port需要sudo 才能運行
	#heroku沒有sudo 的執行權限
	port=int(os.environ["SOCKET_PORT"]) 
	#https://stackoverflow.com/questions/45385384/how-can-i-run-as-root-on-heroku
	socketio.run(app, host="0.0.0.0", port=port, use_reloader=False)
	app.run(host='0.0.0.0',port=8000)
