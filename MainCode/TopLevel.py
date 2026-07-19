from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from datetime import datetime
from .MainClasses import *
from .Style import *

Today=datetime.now()

class CityNameError(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Wrong City Name!")
        self.setGeometry(600,400,100,150)
        self.layout=VBoxLayout(self)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        Label("Re-Enter City Name", Addto=self.layout)
        self.Button = QPushButton("Close")
        self.layout.addWidget(self.Button)

        self.Button.clicked.connect(self.close)

        self.setObjectName("TopLevel")

        ApplyStyles(self)

    


class EnterAPI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Your Weather API and City")
        self.setGeometry(600,400,350,280)
        self.layout=VBoxLayout(self)

        # City Section
        city_group = QGroupBox("City Validation")
        city_layout = QVBoxLayout(city_group)
        
        city_label = Label("Enter City Name", Addto=city_layout)
        self.CityEntered = QLineEdit()
        self.CityEntered.setPlaceholderText("e.g., New York, London, Tokyo")
        city_layout.addWidget(self.CityEntered)
        
        self.CityStatus = QLabel("")
        self.CityStatus.setStyleSheet("color: green; font-weight: bold;")
        city_layout.addWidget(self.CityStatus)
        
        self.layout.addWidget(city_group)

        # API Section
        api_group = QGroupBox("API Key")
        api_layout = QVBoxLayout(api_group)
        
        api_label = Label("Enter Your API Key", Addto=api_layout)
        self.APIEntered = QLineEdit()
        self.APIEntered.setPlaceholderText("Your OpenWeatherMap API key")
        api_layout.addWidget(self.APIEntered)
        
        self.Error = QLabel(
            'Wrong API key, Enter another One! If not, get one from here: '
            '<a href="https://openweathermap.org/guide#openweather_api_overview">Click here</a>'
        )
        self.Error.setTextFormat(Qt.TextFormat.RichText)
        self.Error.setOpenExternalLinks(True)
        self.Error.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.Error.setWordWrap(True)
        self.Error.hide()
        api_layout.addWidget(self.Error)
        
        self.Entered = QPushButton("Confirm API Key")
        api_layout.addWidget(self.Entered)
        
        self.layout.addWidget(api_group)

        self.setObjectName("TopLevel")
        ApplyStyles(self)

    def check_city(self):
        city_name = self.CityEntered.text().strip()
        if not city_name:
            self.CityStatus.setText("Please enter a city name")
            self.CityStatus.setStyleSheet("color: red; font-weight: bold;")
            return
        
        # Create a temporary WeatherFetcher instance to check the city
        # Note: This assumes API key is not required for geocoding, which is correct for OpenWeatherMap
        from .Data import WeatherFetcher
        wf = WeatherFetcher()
        
        if wf.CheckCity(city_name):
            self.CityStatus.setText(f"✓ '{city_name}' is a valid city!")
            self.CityStatus.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.CityStatus.setText(f"✗ '{city_name}' not found. Please check spelling.")
            self.CityStatus.setStyleSheet("color: red; font-weight: bold;")

        






class SearchCityFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Search City")
        #self.resize(750,500)
        self.setGeometry(600,400,250,180)
        self.layout=VBoxLayout(self)

        l=Label("Enter a City",Addto=self.layout)
        self.CityEntered=QLineEdit()
        self.Entered=QPushButton("Search")

        self.layout.addWidget(self.CityEntered)
        self.layout.addWidget(self.Entered)

        self.setObjectName("TopLevel")

        ApplyStyles(self)






class CreateTopLevel(QWidget):
    def __init__(self,city,data: list | str) -> str | None:
        super().__init__()
        self.city=city
        
        if data=="Error":
            self.data={
            "city": self.city,
            "state": "-",
            "country": "-",
            "timezone": "-",
            "current": {
                "temperature_2m": "-",
                "weather_code": "",
                "windspeed_10m": "-",
                "relative_humidity_2m": "-",
                "visibility": "-",
            },
            "daily": {
                "temperature_2m_mean": [f"-" for i in range(7)],
                "weather_code": [f"" for i in range(7)],
                }   
            
            }
            #print("\n\nGoing to pass the function\n\n")
        else:
            self.data=data   #>>>   NEED TO ADJUST IT   <<<#


        self.setWindowTitle(f"{city} Details")
        #self.resize(750,500)
        self.setGeometry(300,100,750,500)
        self.layout=HBoxLayout(self)
        #Label("I am a new Window!",Addto=self.layout)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.Section1Frame=FrameBox(FrameLayout=self.layout)
        self.Section2Frame=FrameBox(FrameLayout=self.layout)


        self.Section1=VBoxLayout(Frame=self.Section1Frame)
        self.Section2=VBoxLayout(Frame=self.Section2Frame)

        self.Section1_Area()
        self.Section2_Area()


        self.Section1Frame.setMinimumWidth(600)

        self.setObjectName("TopLevel")

        ApplyStyles(self)

        



    def Section1_Area(self) -> None:

        self.Section1_TopFrame=FrameBox(FrameLayout=self.Section1)
        self.Section1_Top=HBoxLayout(Frame=self.Section1_TopFrame)
        self.Section1_TopFrame.setMinimumHeight(250)
        self.Section1_MiddleFrame=FrameBox(FrameLayout=self.Section1)
        self.Section1_Middle=HBoxLayout(Frame=self.Section1_MiddleFrame)
        self.Section1_TopFrame.setContentsMargins(24,12,24,12)
        self.Section1_Bottom=HBoxLayout(Addto=self.Section1)


        self.section1_Top_Left=VBoxLayout(Addto=self.Section1_Top)
        self.section1_Top_Left.setSpacing(5)

        self.Temp=Label(f"{self.data["current"]["temperature_2m"]}°C",Addto=self.section1_Top_Left,Name="Large-Text")
        self.Temp.setStyleSheet("padding-bottom:10px")
        self.Date=Label(f"Today   {Today.strftime('%d')}, {Today.strftime('%b')} {Today.strftime('%y')}",Addto=self.section1_Top_Left)
        self.City=Label(self.city,Addto=self.section1_Top_Left)
        self.WeatherStatus=Label(Weather.interpret(self.data["current"]["weather_code"])[1],Addto=self.section1_Top_Left)
        self.WeatherStatus.setStyleSheet("padding-top:10px")

        self.Weather=Label(Weather.interpret(self.data["current"]["weather_code"])[0],Addto=self.Section1_Top,Alignment=CENTER,Name="WeatherIcon-Larger")

        self.Grid=QGridLayout()
        self.Section1_Middle.addLayout(self.Grid)

        #print(self.data["current"]["windspeed_10m"])

        WindSpeed=Label(str(self.data["current"]["windspeed_10m"]),Addto=[self.Grid,0,0],Alignment=CENTER)
        Wind=Label("Wind",Addto=[self.Grid,1,0],Alignment=CENTER)
        Humidity=Label(str(self.data["current"]["relative_humidity_2m"]),Addto=[self.Grid,0,1],Alignment=CENTER)
        HumdiityLevel=Label("Humidity",Addto=[self.Grid,1,1],Alignment=CENTER)
        Visibility=Label(str(self.data["current"]["visibility"]),Addto=[self.Grid,0,2],Alignment=CENTER)
        VisibilityLevel=Label("Visibility",Addto=[self.Grid,1,2],Alignment=CENTER)

        self.Add_To_Quick_View=QPushButton("ADD TO QUICK VIEW")
        self.Make_Main_City=QPushButton("MAKE YOUR MAIN CITY")

        #self.Add_To_Quick_View.setObjectName("Button2")

        self.Add_To_Quick_View.setStyleSheet("background:#CECECE;border:none;color:#2B2B2B;padding:12px 16px 12px 16px;")
        self.Make_Main_City.setStyleSheet("background:#686868;border:none;color:#D5D5D5;padding:12px 16px 12px 16px;")

        self.Section1_Bottom.addWidget(self.Add_To_Quick_View)
        self.Section1_Bottom.addWidget(self.Make_Main_City)

        #self.Make_Main_City.clicked.connect()
    
    def Section2_Area(self):

        self.close=Label("Close...",Addto=self.Section2,Alignment=RIGHT)
        self.setMaximumHeight(80)
        self.close.clicked.connect(self.destroy)

        self.WeekGrid=QGridLayout()
        self.Section2.addLayout(self.WeekGrid)

        for i in range(1,7):

                Label(f"{int(Today.strftime('%d'))+(i+1)} {Today.strftime('%b')}",Addto=[self.WeekGrid,i,0])
                #print(self.data["daily"]["weather_code"][i])
                Label(Weather.interpret(int(self.data["daily"]["weather_code"][i]),self.data["timezone"])[0],Addto=[self.WeekGrid,i,1],Name="WeatherIcon-Smaller")   




if __name__=="__main__":

    CreateTopLevel("Jaipur",None)
    
