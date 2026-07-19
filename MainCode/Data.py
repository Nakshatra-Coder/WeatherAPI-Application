import requests as re
import json
import pickle
from .MainClasses import PATH

class WeatherFetcher:

    geo_url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"

    single_city_url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude={}&longitude={}&"
            "current=temperature_2m,weather_code,windspeed_10m,relative_humidity_2m,visibility&"
            "daily=temperature_2m_mean,weather_code&"
            "timezone=auto"
        )

    main_url = (
                "https://api.open-meteo.com/v1/forecast?"
                "latitude={}&longitude={}&"
                "hourly=temperature_2m,relative_humidity_2m,visibility,precipitation,"
                "windspeed_10m,winddirection_10m,weathercode&"
                "daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean&"
                "timezone=auto"
            )
    

    def __init__(self):
        try:
            with  open(PATH("mainData.bin"),"rb") as f:
                self.API_key=pickle.load(f)
                
        except Exception as e:
            print("Error is:",e)
            self.API_key = False


    def CheckCity(self, Text: str) -> bool:

        try:
            if not self.API_key:
                return False

            response = re.get(
                self.geo_url.format(Text.capitalize().strip("\n"), self.API_key),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                if data.get("cod") in {401, 403, 404} or "message" in data:
                    return False

            if not isinstance(data, list) or len(data) == 0:
                return False

            return True
        except Exception as e:
            print("\nCheck Failed\n", e)
            return False


    def SingleData(self, city: str) -> list | str:
        
        try:
            response = re.get(self.geo_url.format(city.capitalize().strip("\n"), self.API_key))
            DataVar = response.json()

            lat, lon = DataVar[0]["lat"], DataVar[0]["lon"]
            Country, State = DataVar[0].get("country"), DataVar[0].get("state")
            
            main_data = self.BasicData([lat,lon])

            main_data["city"]=city
            main_data["state"]=State
            main_data["country"]=Country

        except Exception as e:
            print("Error:", e)
            main_data = "Error"

        return main_data
    
    def MainCityData(self, city: str) -> list | str:

        try:
            response = re.get(self.geo_url.format(city.capitalize().strip("\n"), self.API_key))
            DataVar = response.json()

            print("Step - 1 : COMPLETED", DataVar)

            lat, lon = DataVar[0]["lat"], DataVar[0]["lon"]
            Country, State = DataVar[0].get("country"), DataVar[0].get("state")

            print("Step - 2 : COMPLETED")

            main_response = re.get(self.main_url.format(lat, lon))
            main_data = main_response.json()

            print("Step - 3 : COMPLETED")

            main_data['country']=Country
            main_data['state']=State
            with open(PATH("Weather.json"),'w') as f:
                json.dump(main_data, f, indent=8)

            print("Step - 4 : COMPLETED")

        except Exception as e:
            print("Error:", e)
            main_data = "Error"

        return main_data

    def BasicData(self, Coords: list) -> dict:

        """
        
        main_data["Details"] = [CITY, STATE, COUNTRY]
        main_data["Current"] = [TEMP, WEATHER_CODE, WIND, HUMIDITY, VISIBILITY]
        main_data["Weekly] = [TEMP, WEATHER_CODE]

        """

        main_response = (re.get(self.single_city_url.format(Coords[0],Coords[1]))).json()
        #print(main_response)

        return self.PrettyPrint_Basic(main_response)
    
    def PrettyPrint_Basic(self, elements: dict) -> dict:
        symbols = {
            "temperature_2m": elements["current_units"]["temperature_2m"],
            "weather_code": elements["current_units"]["weather_code"],
            "windspeed_10m": elements["current_units"]["windspeed_10m"],
            "relative_humidity_2m": elements["current_units"]["relative_humidity_2m"],
            "visibility": elements["current_units"]["visibility"],
            "temperature_2m_mean": elements["daily_units"]["temperature_2m_mean"]
        }

        main = {
            "city": "",
            "state": "",
            "country": "",
            "timezone": elements.get("timezone", ""),
            "current": {
                "temperature_2m": elements["current"]["temperature_2m"],
                "weather_code": elements["current"]["weather_code"],
                "windspeed_10m": elements["current"]["windspeed_10m"],
                "relative_humidity_2m": elements["current"]["relative_humidity_2m"],
                "visibility": elements["current"]["visibility"],
            },
            "daily": {
                "temperature_2m_mean": [f"{i}{symbols['temperature_2m_mean']}" for i in elements["daily"]["temperature_2m_mean"]],
                "weather_code": [str(i) for i in elements["daily"]["weather_code"]],
            }
        }
        return main
    
    def OtherCitiesData(self):

        try:
            cities = {}

            with open(PATH("Cities.txt"),"r") as f:
                city_names = f.readlines()
                cities["MainCity"] = city_names[0].strip("\n")

                if len(city_names) == 1:
                    pass

                else:
                    for city in range(1, len(city_names)):
                        cities[city] = self.SingleData(city_names[city].strip("\n"))

            with open(PATH("CitiesDetails.json"),"w") as f1:
                json.dump(cities, f1, indent = 8)

            for i in range(1,len(city_names)):
                if cities[city] == "Error":
                    raise Exception("Error in Data Retrieving!")

            return True

        except Exception as e:
            print("Error:",e)
            cities = "Error"

            return False
        

class CheckAPI:
    def __init__(self, API, city='Tokyo'):
        self.result = False

        if not API:
            return

        try:
            URL = "https://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"
            response = re.get(URL.format(city, API), timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                if data.get("cod") in {401, 403, 404} or "message" in data:
                    print("Error in API Key or City Name",data)
                    self.result = False
                else:
                    self.result = True
            else:
                self.result = isinstance(data, list) and len(data) > 0

        except Exception:
            self.result = False

    def __bool__(self):

        return self.result



        
if __name__ == "__main__":

    a = CheckAPI(" ")
    print(a.result)

    # A = WeatherFetcher()

    # result = A.CheckCity("Jod235rfasg")
    # print("\n\n",result)
    '''
    result = A.SingleData("Jaipur")
    print("\n\n",result)

    result = A.MainCityData("Delhi")
    print("\n\n",result)

    result = A.OtherCitiesData()
    print("\n\n",result)
    '''  



# WHAT IS H11 MODULE