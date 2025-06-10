import os
import requests
from django.conf import settings

class GoogleBooksAPI:
    BASE_URL = "https://www.googleapis.com/books/v1"
    API_KEY = settings.GOOGLE_BOOKS_API_KEY

    @classmethod
    def search_books(cls, query):
        """Поиск книг по запросу"""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/volumes",
                params={
                    "q": query,
                    "key": cls.API_KEY
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching books: {e}")
            return None

    @classmethod
    def get_book_details(cls, book_id):
        """Получение детальной информации о книге"""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/volumes/{book_id}",
                params={"key": cls.API_KEY}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching book details: {e}")
            return None

class WeatherAPI:
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    API_KEY = settings.OPENWEATHERMAP_API_KEY

    @classmethod
    def get_weather(cls, city):
        """Получение информации о погоде в городе"""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/weather",
                params={
                    "q": city,
                    "appid": cls.API_KEY,
                    "units": "metric",
                    "lang": "ru"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather: {e}")
            return None 