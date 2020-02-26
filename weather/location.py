import openpyxl
import json
from datetime import datetime, timedelta
import urllib.request

serviceKey = '공공데이터 사이트에서 기상청 동네예보 조회서비스의 API 키를 발급받은 후 입력해 주세요'

def getLocationJson():
    
    jsonData = {}
    jsonData["location"] = []

    file = openpyxl.load_workbook("기상청18_동네예보 조회서비스_오픈API활용가이드_격자_위경도.xlsx")
    data = file.active

    for i in range(2, len(data['A'])) :
        tmp = {
            "local" : "{0} {1} {2}".format(
                data['A' + str(i)].value, data['B' + str(i)].value, data['C' + str(i)].value),
            "X" : data['D' + str(i)].value,
            "Y" : data['E' + str(i)].value
        }
        jsonData["location"].append(tmp)

    with open('locationData.json', 'w', encoding='UTF8') as saveFile:
        json.dump(jsonData, saveFile, indent='\t', ensure_ascii=False)

def getBaseTime(hour): 

    hour = int(hour) 
    
    if hour < 3: 
        return '2000' 
    elif hour < 6: 
        return '2300' 
    elif hour < 9: 
        return '0200' 
    elif hour < 12: 
        return '0500' 
    elif hour < 15: 
        return '0800' 
    elif hour < 18: 
        return '1100' 
    elif hour < 21: 
        return '1400' 
    elif hour < 24: 
        return '1700'

def getNowWeatherData(location):

    numOfRows = '8'
    x = location[1]
    y = location[2]
    now = datetime.now()

    baseNow = (now - timedelta(hours = 1))
    baseDate = baseNow.strftime('%Y%m%d')
    baseHour = baseNow.strftime('%H00')

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey={0}&numOfRows={1}&pageNo=1&base_date={2}&base_time={3}&nx={4}&ny={5}&dataType=json'.format(
        serviceKey, numOfRows, baseDate, baseHour, x, y
    )
    request = urllib.request.Request(url)
    data = urllib.request.urlopen(request).read()
    jsonData = json.loads(data)
    
    today = {}
    for i in jsonData['response']['body']['items']['item']:
        today[i['category']]= i['obsrValue']
    return today

def getTodayWeatherData(location):

    numOfRows = '20'
    x = location[1]
    y = location[2]
    now = datetime.now()

    baseNow = (now - timedelta(hours = 1))
    baseDate = baseNow.strftime('%Y%m%d')
    if now.hour < 6: 
        baseDate = (now - timedelta(days = 1)).strftime('%Y%m%d')
    else: 
        baseDate = now.strftime('%Y%m%d')
    
    baseHour = getBaseTime(int(now.strftime('%H')))

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={0}&numOfRows={1}&pageNo=1&base_date={2}&base_time={3}&nx={4}&ny={5}&dataType=json'.format(
        serviceKey, numOfRows, baseDate, baseHour, x, y
    )
    request = urllib.request.Request(url)
    data = urllib.request.urlopen(request).read()
    jsonData = json.loads(data)
    
    today = {}
    fcstTime = jsonData['response']['body']['items']['item'][0]["fcstTime"]
    for i in jsonData['response']['body']['items']['item']:
        if i["fcstTime"] != fcstTime:   
            break
        else:
            today[i['category']]= i['fcstValue']
    return today
    
def getLocation(locations):

    coordinate = []
    tmp = locations.split(' ')
    tmp.reverse()

    jsonFile = open('locationData.json', encoding='utf8').read()
    data = json.loads(jsonFile)

    for j in tmp:
        for i in data["location"]:
            if j in i["local"]:
                coordinate.append(i["local"])
                coordinate.append(i["X"])
                coordinate.append(i["Y"])
                return coordinate

def findPTY(PTY):

    if PTY == '0':
        return '없음'
    elif PTY == '1':
        return '비'
    elif PTY == '2':
        return '비 또는 눈'
    elif PTY == '3':
        return '눈'
    elif PTY == '4':
        return '소나기'
    else:
        return 'ERROR: 알 수 없는 코드'

def findRN(RN):
    rn = float(RN)
    if rn <= 0:
        return '0mm 또는 없음'
    elif rn <= 1:
        return '1mm 미만'
    elif rn <= 5:
        return '1~4mm'
    elif rn <= 10:
        return '5~9mm'
    elif rn <= 20:
        return '10~19mm'
    elif rn <= 40:
        return '20~39mm'
    elif rn <= 70:
        return '40~69mm'
    else:
        return '70mm 이상'

def findSO(SO):
    so = float(SO)
    if so <= 0:
        return '0cm 또는 없음'
    elif so <= 1:
        return '1cm 미만'
    elif so <= 5:
        return '1~4cm'
    elif so <= 10:
        return '5~9cm'
    elif so <= 20:
        return '10~19cm'
    else:
        return '20cm 이상'

def getSKY(SKY):
    if SKY == '1':
        return '맑음'
    elif SKY == '2':
        return '구름 조금'  ## 삭제됨
    elif SKY == '3':
        return '구름 많음'
    elif SKY == '4':
        return '흐림'
    else:
        return 'ERROR: 알 수 없는 코드'

def findVEC(VEC):
    
    vecValue = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
    
    vec = round((int(VEC) + 22.5 * 0.5) / 22.5)

    return vecValue[vec]

if __name__ == '__main__':
    ## getLocationJson()
    lo = input()
    coordinate = getLocation(lo)
    todayNowWeather = getNowWeatherData(coordinate)

    print('{0}의 현재 날씨!'.format(coordinate[0]))
    print('현재 기온: {}℃'.format(todayNowWeather['T1H']))
    print('1시간 내 강수량: {}'.format(findRN(todayNowWeather['RN1'])))
    print('현재 습도: {}%'.format(todayNowWeather['REH']))
    print('풍향풍속: {}, {}m/s'.format(findVEC(todayNowWeather['VEC']), todayNowWeather['WSD']))

    print('-----------------------------------------')

    print('{0}의 오늘 예보!'.format(coordinate[0]))
    todayWeather = getTodayWeatherData(coordinate)

    print('강수 확률: {}%'.format(todayWeather['POP']))
    print('예상되는 강수 형태: {}'.format(findPTY(todayWeather['PTY'])))

    if "R06" in todayWeather:
        print('예상되는 6시간 강수량: {}'.format(findRN(todayWeather['R06'])))

    print('습도: {}%'.format(todayWeather['REH']))

    if "S06" in todayWeather:
        print('예상되는 6시간 적설량: {}'.format(findSO(todayWeather['S06'])))

    print('하늘 형태: {}'.format(getSKY(todayWeather['SKY'])))

    if "TMN" in todayWeather:
        print('아침 최저기온: {}℃'.format(todayWeather['TMN']))
    if "TMX" in todayWeather:
        print('낮 최고기온: {}℃'.format(todayWeather['TMX']))

    print('3시간 기온: {}℃'.format(todayWeather['T3H']))
    print('풍향풍속: {}, {}m/s'.format(findVEC(todayWeather['VEC']), todayWeather['WSD']))

    if "WAV" in todayWeather:
        print('파고: {}M'.format(todayWeather['WAV']))