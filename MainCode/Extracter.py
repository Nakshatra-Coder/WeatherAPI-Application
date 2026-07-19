import json
from .MainClasses import PATH

class Data:

    def __init__(self):

        self.MainCity=open(PATH("Cities.txt"),"r")

        data = self.MainCity.readlines()

        if data == []:
            self.MainCity='Delhi'
        else:
            self.MainCity=data[0].strip("\n")

    def GetData(self,extract_result):
        
        self.extract_result=extract_result

        self.data=None
        self.timezone=None
        self.HourlyData={}
        self.DailyData={}
        self.MainDetails={}
        self.cities={}
        self.read_data()
        self.Details()
        self.Hourly()
        self.Daily()


    def read_data(self):
        with open(PATH("Weather.json"),"r") as f:
            self.data=json.load(f)
            #print(self.data)
            self.timezone=self.data["timezone"]

        with open(PATH("CitiesDetails.json"),"r") as f1:
            data=json.load(f1)
            self.cities["MainCity"]=data["MainCity"].strip("\n")
            if len(data)==0:
                pass
            else:
                for i in range(1,len(data)):
                    self.cities[i]=data[str(i)]

    def Details(self):
        a = ["latitude",
        "longitude",
        "generationtime_ms",
        "utc_offset_seconds",
        "timezone",
        "timezone_abbreviation",
        "elevation"]

        for i in a:
            self.MainDetails[i]=self.data[i]
            

    def Hourly(self):
        self.HourlyData={"temperature_2m":{},"relative_humidity_2m":{},"visibility":{},"precipitation":{},"windspeed_10m":{},"winddirection_10m":{},"weathercode":{}}

        for i in range(7):
            for j in self.HourlyData:
                l=[]
                for k in range(24):
                    if self.extract_result==False:
                        l.append("-"+self.data['hourly_units'][j])
                        continue
                    #self.data["hourly"]["time"][k+(i*24)] => for getting the time and date
                    if j=="weathercode":
                        l.append(self.data["hourly"][j][k+(i*24)])
                    elif j=="temperature_2m":
                        l.append(f"{int(self.data['hourly'][j][k+(i*24)])}{self.data['hourly_units'][j]}")
                    elif j=="visibility":
                        l.append(f"{int(self.data['hourly'][j][k+(i*24)])//1000} km")
                    else:
                        l.append(str(self.data["hourly"][j][k+(i*24)])+self.data["hourly_units"][j])
                self.HourlyData[j][i]=l
        #print(self.HourlyData)

    def Daily(self):
        self.DailyData={"temperature_2m_max":[],"temperature_2m_min":[],"precipitation_sum":[],"relative_humidity_2m_mean":[]}
        for i in self.DailyData:
            if self.extract_result==False:
                self.DailyData[i]=["-" for j in self.data["daily"][i]]
                continue
            self.DailyData[i]=[f"{int(j)}{self.data['daily_units'][i]}" for j in self.data["daily"][i]]
        #print(self.DailyData)
                

if __name__=="__main__":
    Data()
