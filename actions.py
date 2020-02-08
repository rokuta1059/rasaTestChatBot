# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from bs4 import BeautifulSoup
import urllib.request
client_id = "NAVER_CLIENT_ID" # 애플리케이션 등록시 발급 받은 값
client_secret = "NAVER_CLIENT_SECRET" # 애플리케이션 등록시 발급 받은 값

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Get Weather!")

        encText = urllib.parse.quote('춘천시 효자동 날씨')
        url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        bsObj = BeautifulSoup(response, "html.parser")
        todayBase = bsObj.find('div', {'class': 'today_area _mainTabContent'})

        temp = bsObj.find('div', {'class': 'select_box'})
        temp2 = temp.find('em')

        temp = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = temp.text.strip()

        temp = todayBase.find('p', {'class': 'cast_txt'})
        todayCast = temp.text.strip()

        temp = todayBase.find('span', {'class': 'merge'})
        todayMerge = temp.text.strip()

        temp = todayBase.find('span', {'class': 'sensible'})
        temp2 = temp.find('span', {'class': 'num'})
        todaySensible = temp2.text.strip()

        temp = todayBase.find('dl', {'class': 'indicator'})
        temp2 = temp.find_all('dd')
        todayDust = temp2[0].text.strip()

        result = "날씨는 {0}! 기온은 {1}! 최저 최고는 {2}! 체감온도는 {3}! 미세먼지는 {4}!".format(todayTemp, todayCast, todayMerge, todaySensible, todayDust)
        dispatcher.utter_message(result)

        return []

class ActionTemp(Action):

    def name(self) -> Text:
        return "action_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        encText = urllib.parse.quote('춘천시 효자동 날씨')
        url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        bsObj = BeautifulSoup(response, "html.parser")
        todayBase = bsObj.find('div', {'class': 'today_area _mainTabContent'})

        temp = bsObj.find('div', {'class': 'select_box'})

        temp = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = temp.text.strip()

        temp = todayBase.find('span', {'class': 'sensible'})
        temp2 = temp.find('span', {'class': 'num'})
        todaySensible = temp2.text.strip()

        result = "기온은 {0}! 체감온도는 {1}!".format(todayTemp, todaySensible)
        dispatcher.utter_message(result)

        return []

class ActionTomorrowTemp(Action):

    def name(self) -> Text:
        return "action_tomorrow_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        encText = urllib.parse.quote('춘천시 효자동 날씨')
        url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        bsObj = BeautifulSoup(response, "html.parser")

        temp = bsObj.find('div', {'class': 'select_box'})
        temp2 = temp.find('em')

        tomorrowBase = bsObj.find_all('div', {'class': 'main_info morning_box'})

        temp = tomorrowBase[0].find('span', {'class': 'todaytemp'})
        tomorrowTemp = temp.text.strip()

        temp = tomorrowBase[0].find('ul', {'class': 'info_list'})
        temp2 = temp.find('p', {'class': 'cast_txt'})
        tomorrowWeather = temp2.text.strip()

        result = "내일날씨 {0}! 온도는 {1}!".format(tomorrowWeather, tomorrowTemp)
        dispatcher.utter_message(result)

        return []