# rasaTestChatBot

rasa를 이용한 날씨 정보를 알려주는 간단한 챗봇입니다.     
본 프로그램은 https://github.com/CS408-WorkoutBuddy/WorkoutBuddy에서 일부 발췌하였습니다.

## 기본 환경 구축

### 1. 기본 생성 및 구축

1.1. conda를 이용해 새로운 가상환경을 만듭니다.

> conda create -n {가상환경 이름} python=3.6.9

> conda activate {가상환경 이름}

> pip install rasa[spacy]==1.3.9  

> pip install -r requirements.txt

1.2. rasa 실행 환경을 구축합니다.  

> python -m spacy download en_core_web_md  

> python -m spacy link en_core_web_md en 

### 2. RASA pipeline 한글화

상단의 [링크](https://github.com/CS408-WorkoutBuddy/WorkoutBuddy)의 **2. RASA pipeline 한글화**를 참고하여 진행하여 주시기 바랍니다.

### 3. 수정 및 실행

3.1. API 키를 입력합니다.

- [공공데이터 포털](https://www.data.go.kr/)의 [기상청 날씨예보 정보](https://www.data.go.kr/dataset/15000099/openapi.do)에서 API 키를 발급받습니다.

- 발급받은 키를 weather/location.py의 serviceKey에 입력합니다.

3.2. 원하는 지역을 설정합니다.

- actions.py의 내용을 수정합니다. "춘천"에 해당하는 부분을 원하는 지역으로 수정합니다.

```python
    ## 원하는 위치로 수정 가능
    coordinate = weather.getLocation("춘천")
    nowWeather = weather.getNowWeatherData(coordinate)
```

3.3. 해당 폴더에서 ```rasa shell``` 명령어를 실행합니다.

3.4. 해당 폴더에서 ```rasa run actions``` 명령어를 실행합니다.