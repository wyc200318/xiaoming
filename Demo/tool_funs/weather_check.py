"""
更简单的单参数输入工具实现，用于查询现在天气的情况
"""
# from langchain_core.pydantic_v1 import *
from pydantic import BaseModel, Field
import requests


def weather(location: str, api_key: str):
    """
    定义当前工具对应的执行逻辑
    :param location:
    :param api_key:
    :return:
    """
    print(f"天气查询:{location} - {api_key}")
    url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["results"][0]["now"]["temperature"],
            "description": data["results"][0]["now"]["text"],
        }
        return weather
    else:
        raise Exception(
            f"Failed to retrieve weather: {response.status_code}")


def weathercheck(location: str):
    return weather(location, "SqWCDI5TuUyD4Nbby")   # StkFQ0VKHJ524OnyO


class WeatherInput(BaseModel):
    location: str = Field(description="city name")
