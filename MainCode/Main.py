import sys
import datetime as dt

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt6.QtCore import Qt

from .MainClasses import *
from .Widgets import *
from .Style import ApplyStyles
from .TopLevel import CreateTopLevel, SearchCityFrame, EnterAPI, CityNameError
from .Data import WeatherFetcher, CheckAPI
from .UpdateData import Update

import MainCode.Extracter as Extracter

sys.path.insert(0,'MainCode\\')

class MainWindow(QMainWindow):
        def __init__(self,mode="online"):
                super().__init__()

                self.setWindowTitle("Weather Application")
                self.setGeometry(30,35,1300,700)

                self.mode="online"
                
                print("Proceeding with dataqueue")
                self.DataQueue()

                self.MainCity=self.CityLoader.MainCity
                self.Today=dt.datetime.now()  


                self.Main_Area()
                ApplyStyles(self)

        def DataQueue(self):

                self.wf = WeatherFetcher()

                self.wf.OtherCitiesData()
                self.CityLoader=Extracter.Data()
                print("This is the cityloader value: ",self.CityLoader.MainCity)
                self.result = self.wf.MainCityData(self.CityLoader.MainCity)

                if self.result == "Error" and self.mode == "online":
                        
                        print("Data can't be fetched")
                        #IF WANT TO USE OFFLINE COMMMENT THE BELOW LINE...
                        self.ShowError()



        def Main_Area(self):

                self.WorkSpace=QWidget()
                self.WorkSpace.setContentsMargins(10,10,10,10)
                self.setCentralWidget(self.WorkSpace)

                self.MainLayout=HBoxLayout(self.WorkSpace)

                self.Region()

        def Region(self):

                #print("\n\n\n",self.CityLoader, self.result, self.MainCity)

                CreateGlobal(self,DataExtractor(self.CityLoader, self.result), self.MainCity)

                self.LeftArea = Left_Region()
                self.RightArea = Right_Region()

                self.RegionEvents()

                self.MainLayout.addWidget(self.LeftArea)
                self.MainLayout.addWidget(self.RightArea)

        def RegionEvents(self):

                self.LeftArea.addcity.Layout2Frame.clicked.connect(self.SearchCityFunction)
                self.RightArea.frame1.SearchTab.returnPressed.connect(lambda: self.SearchCityCheck(self.RightArea.frame1.SearchTab.text()))
                
        def SearchCityFunction(self):


                self.CreateSearchFrame = SearchCityFrame()
                self.CreateSearchFrame.show()
                
                self.CreateSearchFrame.Entered.clicked.connect(lambda: self.SearchCityCheck(self.CreateSearchFrame.CityEntered.text()))

        def SearchCityCheck(self,city):

                #print("Name: ",city)

                if self.wf.CheckCity(city):

                        #print("\nError Check Passes\n")
                        
                        self.CreateCityFrame(city)
                        try:
                                self.CreateSearchFrame.destroy()
                        except:
                                pass

                else:
                        #Error Screen
                        #print("Error: Wrong City Name!")
                        self.CityError=CityNameError()
                        self.CityError.exec()


        def CreateCityFrame(self, city):

                main_data = self.wf.SingleData(city)

                #print("\nSearchedCityData:",main_data)

                self.create = CreateTopLevel(city, main_data)
                #print(self.create)
                self.create.show()

                self.create.Make_Main_City.clicked.connect(lambda:self.UpdateApp(city))
                self.create.Add_To_Quick_View.clicked.connect(lambda:self.UpdateQuickView(city))

        def UpdateQuickView(self, city):

                self.mainData_path = os.path.join(current_dir,"DataStorage","mainData.bin")
                self.Cities_path = os.path.join(current_dir,"DataStorage","Cities.txt")

                with open(self.Cities_path,"r") as f:

                        data = f.readlines()

                if f"{city}\n" in data:

                        print("Already in Quick view!")

                else:

                        with open(self.Cities_path,"a") as f:

                                f.write(f"{city.title()}\n")

                        a = OtherCity(self.LeftArea._1,self.wf.SingleData(city))

                

        def UpdateApp(self, city):

                self.MainLayout.removeWidget(self.LeftArea)
                self.MainLayout.removeWidget(self.RightArea)

                self.LeftArea.deleteLater()
                self.RightArea.deleteLater()

                self.MainCity = city

                update_maincity = Update.MainCity(self,city)

                self.DataQueue()
                self.MainCity=self.CityLoader.MainCity
                try:
                        self.create.destroy()
                finally:
                        self.Region()

        def Reload(self):

                self.UpdateApp(self.MainCity)

        def ShowError(self):

                dialog = DataErrorWindow(self)

                result = dialog.exec()

                if result==QDialog.DialogCode.Accepted:
                        self.wf = WeatherFetcher()
                        self.wf.OtherCitiesData()

                        success = self.wf.MainCityData(self.CityLoader.MainCity)

                        if not success:
                                self.ShowError()
                        else:
                                pass
                
                else:
                        self.close()



class DataErrorWindow(QDialog):
        def __init__(self, parent=None):

                super().__init__(parent)
                self.setWindowTitle("Netork Error!")
                self.setModal(True)
                #print("Entered")

                self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

                layout=QVBoxLayout()
                self.label=Label("Network error occurred.\nCheck your connection.")
                layout.addWidget(self.label)
                btn_layout=QHBoxLayout()
                retry=QPushButton("Try Again")
                close=QPushButton("Close")

                close.clicked.connect(lambda: exit())

                btn_layout.addWidget(retry)
                btn_layout.addWidget(close)

                layout.addLayout(btn_layout)

                self.setLayout(layout)



class DataExtractor:
        def __init__(self,data1,extract_result):

                self.data1=data1
                self.data1.GetData(extract_result)

                self.Details=self.data1.MainDetails
                self.Hourly=self.data1.HourlyData
                self.Daily=self.data1.DailyData
                self.Cities=self.data1.cities

                self.Current={"timezone":self.data1.timezone,"country":self.data1.data["country"],"state":self.data1.data["state"],"Temp":self.Hourly["temperature_2m"][0][int(Today.strftime("%H"))],"status":self.Hourly["weathercode"][0][int(Today.strftime("%H"))],"Humidity":self.Hourly["relative_humidity_2m"][0][int(Today.strftime("%H"))],"Visibility":self.Hourly["visibility"][0][int(Today.strftime("%H"))],"wind":self.Hourly["windspeed_10m"][0][int(Today.strftime("%H"))]}#get the current details
                print(self.Current)



class Run:
        def __init__(self):

                self.app=QApplication(sys.argv)

                #self.Main()

                
                self.wf = WeatherFetcher()
                #print(self.wf.API_key)
                if self.wf.API_key == False: 
                        self.APITopLevel = EnterAPI()
                        self.APITopLevel.show()
                        #print(10)
                        self.APITopLevel.Entered.clicked.connect(self.Proceed)       
                        #print(100)

                else: self.Main()
                                

                self.app.exec()

        def Main(self):
                print("in Main")

                window=MainWindow()
                window.show()

        def Proceed(self):

                #print(10)

                result = CheckAPI(self.APITopLevel.APIEntered.text(),self.APITopLevel.CityEntered.text())

                #print(result.result)

                if result.result == True:
                        #print(self.APITopLevel.APIEntered.text())
                        Updating_data = Update.API(self, self.APITopLevel.APIEntered.text())
                        Updating_Maincity = Update.MainCity(self,self.APITopLevel.CityEntered.text())
                        #print(1)
                        self.APITopLevel.destroy()
                        #print(2)
                        self.APITopLevel.deleteLater()
                        #print(3)
                        window=MainWindow()
                        window.show()
                else: 
                        self.APITopLevel.APIEntered.setText("")
                        self.APITopLevel.Error.setVisible(True)

                
        
                
        



if __name__=="__main__":

        app=QApplication(sys.argv)
        window=MainWindow()
        window.show()
        app.exec()
