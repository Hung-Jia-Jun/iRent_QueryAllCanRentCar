import requests
import json
import configparser

class startQuery:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('Config.ini')

		#讀取身分證字號
		IDNumber = str(config.get(
			'identifyInformation', 'IDNO'))

		#讀取手機ID
		DeviceID = str(config.get(
			'identifyInformation', 'DeviceID'))
		self.query_data = {
                    "para": {
                        "app": "1",
                        "ProjType": "0",
                        "StationID": "X0KI",
                        "SD": "",
                        "InvoiceName": "",
                        "City": "1",
                        "appVersion": "3.0.29",
                        "ED": "",
                        "StationName": "",
                        "IDNO": IDNumber,
                        "ProjID": "P735",
                        "InvoiceTitle": "",
                        "ZipCode": "",
                        "CarTypeName": "",
                        "email": "",
                        "CarNo": "",
                        "InvoiceType": 2,
                        "InvoiceAddress": "",
                        "ProName": "",
                        "CarType": "",
                        "RStationID": "X1UY",
                        "InvoiceBNO": "",
                        "RStationName": "",
                        "DeviceID":DeviceID
                    }
                }

	def getCar(self, Starttime, EndTime, CarType, StationName, StationID, stationGIS,stationAddr):
		self.query_data['para']["SD"] = Starttime
		self.query_data['para']["ED"] = EndTime
		self.query_data['para']["CarType"] = CarType
		#租賃站點名稱
		self.query_data['para']["StationName"] = StationName
		#租賃站點
		self.query_data['para']["StationID"] = StationID
		#還車站點
		self.query_data['para']["RStationID"] = StationID
		# 將資料加入 POST 請求中
		r = requests.post(
			'https://irent.irentcar.com.tw/iMotoAPI/api/CheckBookingStatus', json=self.query_data)
		
		queryBookingCar = json.loads(r.text)
		# "ErrorCode": "ERR263"
		#      此車型，不在所選擇的據點或優惠專案內
		if queryBookingCar["ErrorCode"] != '000000':
			return "StationName:{0} ErrMsg:{1}".format(StationName[0:10],queryBookingCar["ErrMsg"])
		hasCar = queryBookingCar["data"]["hasCar"]

		stationInfo = {}
		#有車就輸出地點與車型
		if hasCar == 1:
			stationInfo["StationName"] = StationName
			stationInfo["StationID"] = StationID
			stationInfo["stationGIS"] = stationGIS
			stationInfo["stationAddr"] = stationAddr
			return stationInfo
		else:
			return None
if __name__ == "__main__":
	StationName = "iRent台北車站[西區平面停車場]"
	Starttime = "20201028151500"
	EndTime = "20201028171500"
	CarType = "001601"
	StationID = "X0KV"
	startQuery = startQuery()
	startQuery.getCar(Starttime, EndTime, CarType,StationName, StationID)
