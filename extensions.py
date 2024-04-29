import requests
import json


class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{base}'
            response = requests.get(url)
            data = json.loads(response.text)
            price = data['rates'][quote] * amount
            return price
        except KeyError:
            raise APIException(f'Указанный неверный код валюты: {quote}')
        except Exception as e:
            raise APIException(f'Произошла ошибка: {str(e)}')
