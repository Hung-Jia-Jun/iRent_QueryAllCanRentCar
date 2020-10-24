import requests
import json
from BookingCar import startQuery
import configparser
class queryStationList:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('Config.ini')

		#讀取手機ID
		DeviceID = str(config.get(
				'identifyInformation', 'DeviceID'))
		self.my_data = {
			"para": {
				"app": "1",
				"ProjID": "ALL",
				"ProjMode": 0,
				"appVersion": "3.0.29",
				"DeviceID": DeviceID
			}
		}

	def searchPark(self, CarType):
		#租賃站的名稱
		stationNameLi = []
		#租賃站ID
		stationIDLi = []

		#
		# 將資料加入 POST 請求中
		r = requests.post(
			'https://irent.irentcar.com.tw/iMotoAPI/api/Preferential', json=self.my_data)
		stations = json.loads(r.text)

		#要查詢租車一定要專案ID
		projID = stations["data"][1]["ProjID"]
		#選擇台北市同站租還專案
		for station in stations["data"][1]["Station"]:
			#因為總共有一千多個站點，那就先以台北市為主
			if station["Area"] == "台北市":
				#租車站地址
				addr = station["ADDR"]
				#租車站ID
				siteID = station["Site_ID"]

				#租賃站點的中文名稱
				SiteName = station["SiteName"]

				#可以輸出站點資訊
				# print("SiteName:{0} Addr:{1} siteID:{2}".format(SiteName , addr, siteID))
				
				#增加篩選車型功能，如果該站點沒有該車型，那就不要去詢問有沒有車
				for car in station["CarType"]:
					if car["TypeID"] == CarType:
						carID = car["TypeID"]
						typeName = car["TypeName"]
						#有該車型，那就加入搜尋的停車場列表
						stationNameLi.append(SiteName)
						stationIDLi.append(siteID)

						#依照各車型輸出詳情
						# print("CarID:{0} TypeName:{1}".format(carID,typeName))
		return stationNameLi, stationIDLi

	def start(self,startQuery,Starttime,EndTime,CarType):
		#將所有的租賃站ID跟名稱列出來
		stationNameLi, stationIDLi = self.searchPark(CarType)
		index = 0
		hasCarStation = []
		print ("以下為有車站點：")
		for stationName in stationNameLi:
			StationName = stationName
			StationID = stationIDLi[index]
			result = startQuery.getCar(Starttime, EndTime, CarType, StationName, StationID)
			if result != None:
				hasCarStation.append(result)
			index += 1
		#回傳有車的站點
		return hasCarStation
if __name__ == "__main__":
	queryStationList = queryStationList()
	startQuery = startQuery()
	queryStationList.start(startQuery)
