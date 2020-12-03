import requests
import json
from BookingCar import startQuery
import configparser
import os
from tqdm import tqdm
class queryStationList:
	def __init__(self):
		if "isHeroku" in os.environ:
			IDNumber = os.environ["IDNO"]
			DeviceID = os.environ["DeviceID"]
			print (IDNumber)
			print (DeviceID)
		else:
			config = configparser.ConfigParser()
			config.read('Config.ini')

			#讀取身分證字號
			IDNumber =str(config.get(
				'identifyInformation', 'IDNO'))
			#讀取手機ID
			DeviceID =str(config.get(
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

	def searchPark(self, CarType,CityName):
		#租賃站的名稱
		stationNameLi = []
		#租賃站ID
		stationIDLi = []

		#station
		stationGISLi = []

		stationAddr = []
		# 將資料加入 POST 請求中
		r = requests.post(
			'https://irent.irentcar.com.tw/iMotoAPI/api/Preferential', json=self.my_data)
		stations = json.loads(r.text)
		if "ErrorCode" in stations:
			if stations["ErrorCode"] != "000000":
				return stations["ErrMsg"]
		#要查詢租車一定要專案ID
		projID = stations["data"][1]["ProjID"]
		#選擇不同縣市的同站租還專案
		for station in stations["data"][1]["Station"]:
			if station["Area"] == CityName:
				#租車站地址
				addr = station["ADDR"]
				#租車站ID
				siteID = station["Site_ID"]

				#租賃站點的中文名稱
				SiteName = station["SiteName"]
				lat, lng = station["Lat"], station["Lng"]
				ADDR = station["ADDR"]
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
						stationGISLi.append([lat, lng])
						stationAddr.append(ADDR)
						#依照各車型輸出詳情
						# print("CarID:{0} TypeName:{1}".format(carID,typeName))
		return stationNameLi, stationIDLi, stationGISLi,stationAddr

	def start(self,startQuery,Starttime,EndTime,CarType,CityName):
		try:
			#將所有的租賃站ID跟名稱列出來
			stationNameLi, stationIDLi, stationGISLi, stationAddr = self.searchPark(
				CarType, CityName)
		except ValueError:
			#返回錯誤，可能是請先登入等驗證問題
			return self.searchPark(CarType, CityName)
		index = 0
		hasCarStation = []
		for stationName in tqdm(stationNameLi):
			StationName = stationName
			StationID = stationIDLi[index]
			#座標位置
			stationGIS = stationGISLi[index]

			Addr = stationAddr[index]
			result = startQuery.getCar(
				Starttime, EndTime, CarType, StationName, StationID, stationGIS,Addr)
			if result != None:
				if "ErrMsg" in result:
					yield result["ErrMsg"]
				hasCarStation.append(result)
			index += 1
			yield len(stationNameLi),hasCarStation
		#回傳有車的站點
		yield len(stationNameLi),hasCarStation
if __name__ == "__main__":
	queryStationList = queryStationList()
	startQuery = startQuery()
	queryStationList.start(startQuery)
