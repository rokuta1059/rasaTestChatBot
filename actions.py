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

import weather

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ## 원하는 위치로 수정 가능
        coordinate = weather.getLocation("춘천")
        nowWeather = weather.getNowWeatherData(coordinate)

        result = "{0}의 현재 날씨는! 기온 {1}℃, 습도 {2}, 풍향풍속: {3}, {4}m/s".format(
            coordinate[0],nowWeather['T1H'], nowWeather['REH'], weather.findVEC(nowWeather['VEC']), nowWeather['WSD'])
        dispatcher.utter_message(result)

        return []

class ActionTemp(Action):

    def name(self) -> Text:
        return "action_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ## 원하는 위치로 수정 가능
        coordinate = weather.getLocation("춘천")
        nowWeather = weather.getNowWeatherData(coordinate)
        todayWeather = weather.getTodayWeatherData(coordinate)
        
        result = "현재 기온은 {}℃!".format(
            nowWeather['T1H']
        )
        dispatcher.utter_message(result)

        result = "앞으로 예상 기온은 {}℃!".format(
            todayWeather['T3H']
        )
        dispatcher.utter_message(result)

        if "TMN" in todayWeather:
            result = "아침 최저 기온은 {}℃!".format(
                todayWeather['TMN']
            )
            dispatcher.utter_message(result)

        if "TMX" in todayWeather:
            result = "낮 최고 기온은 {}℃!".format(
                todayWeather['TMX']
            )
            dispatcher.utter_message(result)

        return []

class ActionNextTemp(Action):

    def name(self) -> Text:
        return "action_next_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coordinate = weather.getLocation("춘천")
        nowWeather = weather.getNowWeatherData(coordinate)
        todayWeather = weather.getTodayWeatherData(coordinate)

        dispatcher.utter_message('{0}의 현재 날씨!'.format(coordinate[0]))
        dispatcher.utter_message('현재 기온: {}℃'.format(nowWeather['T1H']))
        dispatcher.utter_message('1시간 내 강수량: {}'.format(weather.findRN(nowWeather['RN1'])))
        dispatcher.utter_message('현재 습도: {}%'.format(nowWeather['REH']))
        dispatcher.utter_message('풍향풍속: {}, {}m/s'.format(weather.findVEC(nowWeather['VEC']), nowWeather['WSD']))

        dispatcher.utter_message('-----------------------------------------')

        dispatcher.utter_message('{0}의 오늘 예보!'.format(coordinate[0]))

        dispatcher.utter_message('강수 확률: {}%'.format(todayWeather['POP']))
        dispatcher.utter_message('예상되는 강수 형태: {}'.format(weather.findPTY(todayWeather['PTY'])))

        if "R06" in todayWeather:
            dispatcher.utter_message('예상되는 6시간 강수량: {}'.format(weather.findRN(todayWeather['R06'])))

        dispatcher.utter_message('습도: {}%'.format(todayWeather['REH']))

        if "S06" in todayWeather:
            dispatcher.utter_message('예상되는 6시간 적설량: {}'.format(weather.findSO(todayWeather['S06'])))

        dispatcher.utter_message('하늘 형태: {}'.format(weather.getSKY(todayWeather['SKY'])))

        if "TMN" in todayWeather:
            dispatcher.utter_message('아침 최저기온: {}℃'.format(todayWeather['TMN']))
        if "TMX" in todayWeather:
            dispatcher.utter_message('낮 최고기온: {}℃'.format(todayWeather['TMX']))

        dispatcher.utter_message('3시간 기온: {}℃'.format(todayWeather['T3H']))
        dispatcher.utter_message('풍향풍속: {}, {}m/s'.format(weather.findVEC(todayWeather['VEC']), todayWeather['WSD']))

        if "WAV" in todayWeather:
            dispatcher.utter_message('파고: {}M'.format(todayWeather['WAV']))

        return []