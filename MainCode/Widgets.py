from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QRegion, QPainterPath
from .MainClasses import *
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import os
import re
from .TopLevel import CreateTopLevel

Today=dt.datetime.now()
current_dir = os.path.dirname(os.path.abspath(__file__))


class CreateGlobal:
        def __init__(self, main, Info, City):

                global CityData, MainCity, MainClass
                CityData = Info
                MainCity = City
                MainClass = main
                

def ImagePath(file_name):

        Image_Path = os.path.join(current_dir,"Images",file_name)

        return Image_Path


class DisplayedCity(FrameBox):
        def __init__(self,Layout,city,time=None):
                Today=TimeZone(CityData.Current["timezone"])
                Today=Today.current_time
                super().__init__("DisplayedCity")
                super().setFixedHeight(360)
                Layout.addWidget(self)
                BoxLayout=VBoxLayout(self)

                Upper=HBoxLayout(Addto=BoxLayout)
                Datetime=HBoxLayout(Addto=Upper)
                Layout2=VBoxLayout(Addto=Datetime)

                self.Date=Label(f"Today   {Today.strftime('%d')}, {Today.strftime('%b')} {Today.strftime('%y')}",Addto=Layout2)
                self.City=Label(city,Addto=Layout2)
                self.Time=Label(f"{Today.strftime('%I:%M %p')}",Addto=Datetime,Name="Time",Alignment=TOP_RIGHT)

                MiddleFrame=FrameBox(FrameLayout=BoxLayout,margin=False)
                Middle=HBoxLayout(Frame=MiddleFrame)
                MiddleFrame.setMinimumHeight(120)
                self.weather=Label(Weather.interpret(CityData.Current["status"])[0],Addto=Middle,Name="WeatherIcon")
                CityWeather=VBoxLayout(Addto=Middle)
                CityWeather.setSpacing(20)

                self.Temp=Label(CityData.Current["Temp"],Addto=CityWeather,Name="Large-Text")
                self.Condition=Label(Weather.interpret(CityData.Current["status"])[1],Addto=CityWeather)

                Lower=HBoxLayout(Addto=BoxLayout)
                Grid=QGridLayout()
                [Grid.setColumnStretch(i,1) for i in range(3)]
                Grid.setAlignment(CENTER)
                Lower.addLayout(Grid)

                WindSpeed=Label(CityData.Current["wind"],Addto=[Grid,0,0],Alignment=CENTER)
                Wind=Label("Wind",Addto=[Grid,1,0],Alignment=CENTER)
                Humidity=Label(CityData.Current["Humidity"],Addto=[Grid,0,1],Alignment=CENTER)
                HumdiityLevel=Label("Humidity",Addto=[Grid,1,1],Alignment=CENTER)
                Visibility=Label(CityData.Current["Visibility"],Addto=[Grid,0,2],Alignment=CENTER)
                VisibilityLevel=Label("Visibility",Addto=[Grid,1,2],Alignment=CENTER)


class AddCityOption(FrameBox):
        def __init__(self,layout,city_layout):
                super().__init__(margin=True)

                self.Layout2Frame=FrameBox(FrameLayout=layout,margin=False)
                self.Layout2Frame.setObjectName("BaseBoxes1")
                Layout2=HBoxLayout(Frame=self.Layout2Frame)
                self.Layout2Frame.setMinimumHeight(80)

                I=Image("AddImage",ImagePath("Add.png"),Layout2,[30,30])
                I.setMaximumHeight(50)
                I.setMaximumWidth(50)
                

                Label("Add the city you are interested in...",Layout2) 

                self.Layout2Frame.mouseDoubleClickEvent

                #wf=Data.WeatherFetcher()
                #dataCity=wf.SingleData(["Jodhpur"])
                #OtherCity(city_layout,dataCity)
                #print(dataCity)



class OtherCity(FrameBox):
        def __init__(self,Layout,data):
                super().__init__(margin=False)

                self.data=data

                self.setObjectName("BaseBoxes1")
                self.setMaximumHeight(100)
                self.setMinimumHeight(80)
                self.setFixedWidth(380)
                Layout.addWidget(self)
                Container=HBoxLayout(Addto=self)
                Container.setObjectName("AddCityBox")

                self.clicked.connect(self.CityScreen)

                City=data["city"]
                WeatherCode=Weather.interpret(data['current']['weather_code'],data['timezone'])
                Condition=WeatherCode[1]
                Temp=str(data['current']['temperature_2m'])+'°C'
                icon=WeatherCode[0]


                WeatherIcon=Label(icon,Name="WeatherIcon-Smaller",Addto=Container,Alignment=CENTER)

                Layout2Frame=FrameBox(FrameLayout=Container,margin=False)
                Layout2=VBoxLayout(Frame=Layout2Frame)
                Layout2Frame.setMaximumHeight(60)

                OtherCity=Label(City,Name="CityName",Addto=Layout2)
                OtherCondition=Label(Condition,Addto=Layout2)
                OtherTemp=Label(Temp,Name="OtherCityTemp",Addto=Container)

        def CityScreen(self):

                self.screen = CreateTopLevel(self.data["city"], self.data)
                self.screen.show()

                self.screen.Make_Main_City.clicked.connect(self.DestroyTopLevel)

        def DestroyTopLevel(self):

                self.screen.destroy()
                MainClass.UpdateApp(self.data['city'])





                



class Left_Region(QWidget):
        
        

        def __init__(self):
                
                super().__init__()
                self.setFixedWidth(400)
                self.city=MainCity

                LeftLayout=VBoxLayout(self)

                self.frame1=DisplayedCity(LeftLayout,self.city)

                scroll=QScrollArea()
                scroll.setWidgetResizable(1)
                scroll.setFrameShape(QFrame.Shape.NoFrame)
                scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

                scroll.verticalScrollBar().setSingleStep(15)

                scroller=QScroller.scroller(scroll.viewport())
                scroller.grabGesture(scroll.viewport(),QScroller.ScrollerGestureType.LeftMouseButtonGesture)
                pros=scroller.scrollerProperties()
                pros.setScrollMetric(QScrollerProperties.ScrollMetric.FrameRate,60)





                scroll_content=QWidget()
                scroll_content.setObjectName("Scroll")
                scroll_layout=QVBoxLayout(scroll_content)
                scroll_layout.setContentsMargins(0,8,0,0)

                scroll_layout.addStretch()
                scroll.setWidget(scroll_content)
                LeftLayout.addWidget(scroll)

                self._1=VBoxLayout(Addto=scroll_layout)
                _2=VBoxLayout(Addto=scroll_layout)
                _2.setObjectName("AddCityBox")

                for i in range(1,len(CityData.Cities)):
                        if CityData.Cities[i]=="Error":
                                continue
                        else:
                                othercity=OtherCity(self._1,CityData.Cities[i])

                self.addcity=AddCityOption(_2,self._1)

                

                

                
                '''city2=OtherCity(scroll_layout,"NewYork","22°C","Sunny","🌤️")
                city3=OtherCity(scroll_layout,"Moscow","12°C","Cloudy","☁️")
                city3=OtherCity(scroll_layout,"Tokyo","28°C","Cloudy","🌤️")
                city3=OtherCity(scroll_layout,"Delhi","21°C","Cloudy","☁️")
                city3=OtherCity(scroll_layout,"Vatican City","8°C","Cloudy","☁️")'''



class HeroSection(QWidget):
        def __init__(self,Layout):
                super().__init__()
                self.setContentsMargins(0,0,0,0)
                Layout.addWidget(self)
                self.setFixedHeight(80)

                BoxLayout=HBoxLayout(self)
                BoxLayout.setContentsMargins(0,0,0,0)

                SearchArea=FrameBox(Name="SearchArea",FrameLayout=BoxLayout,margin=False)
                SearchLayout=HBoxLayout(Frame=SearchArea)
                SearchArea.setFixedHeight(60)

                Image(None,ImagePath("Search.png"),SearchLayout)

                self.SearchTab=QLineEdit()
                self.SearchTab.setObjectName("SearchTab")
                self.SearchTab.setPlaceholderText("search City...")
                SearchLayout.addWidget(self.SearchTab)


                

                #Image(None,ImagePath("Dark_mode.png"),Scale=[30,30],Layout=BoxLayout)



class Week_data(FrameBox):
        def __init__(self,Layout,city):
                super().__init__(margin=False)
                Layout.addWidget(self)
                self.setMaximumHeight(240)
                BoxLayout=VBoxLayout(self)
                BoxLayout.setContentsMargins(10,10,10,10)
                BoxLayout.setSpacing(8)

                Middle=HBoxLayout(Addto=BoxLayout)

                MainFrame=FrameBox("MiddleLeft",FrameLayout=Middle,margin=False)
                Main=VBoxLayout(Frame=MainFrame)
                Main.setContentsMargins(12,10,12,10)
                Main.setSpacing(8)

                Title=Label(f"Next 7 Days | {city}",Addto=Main,Name="CityName")
                Title.setStyleSheet("padding:0px")

                grid=QGridLayout()
                grid.setSpacing(5)
                grid.setContentsMargins(0,0,0,0)
                Main.addLayout(grid)

                days=['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
                temp=14

                for i in range(7):
                        day=(days.index(Today.strftime("%a"))+i)%7
                        
                        # Day name with full name
                        day_label=QLabel(f"{['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][day]}")
                        day_label.setStyleSheet("color: #eee; font-weight: 600;")
                        grid.addWidget(day_label,i,0)
                        
                        # Temperature and status combined

                        weather_label=QLabel(CityData.Daily["temperature_2m_min"][i])
                        weather_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                        weather_label.setStyleSheet("color: #aaa; font-size: 10px;")
                        grid.addWidget(weather_label,i,1)
                        
                        # Status
                        status_label=QLabel(CityData.Daily["temperature_2m_max"][i])
                        status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                        status_label.setStyleSheet("color: #ccc; font-weight: 600;")
                        grid.addWidget(status_label,i,2)
                        
                        # Set column stretch - day name takes majority
                        if i==0:
                                grid.setColumnStretch(0, 2)
                                grid.setColumnStretch(1, 1)
                                grid.setColumnStretch(2, 1)


class MapWidget(QLabel):
        def __init__(self,parent=None):
                super().__init__(parent)
                self.setFixedSize(400,200)

                dir=os.path.dirname(os.path.abspath(__file__))

                PATH=os.path.join(dir,"Images","world_map.png")

                self.original_pixmap=QPixmap(PATH).scaled(400,200,Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)

                self.setPixmap(self.original_pixmap)
                self.apply_rounded_corners(20)

        def mark_location(self,lat,lon):

                canvas = self.original_pixmap.copy()
                painter=QPainter(canvas)

                x=int(((lon+180)*400)/360)-9

                y=int(((90-lat)*200)/180)+16

                painter.setBrush(QColor("red"))
                painter.setPen(QPen(Qt.GlobalColor.black,1))
                painter.drawEllipse(x-3,y-3,6,6)

                painter.end()
                self.setPixmap(canvas)

        def apply_rounded_corners(self,radius):

                path = QPainterPath()
                path.addRoundedRect(0,0,self.width(),self.height(), radius, radius)

                region = QRegion(path.toFillPolygon().toPolygon())
                self.setMask(region)




class ExtraBox(FrameBox):
        def __init__(self,Layout):
                super().__init__(margin=False)
                Layout.addWidget(self)
                self.setMaximumHeight(240)
                BoxLayout=VBoxLayout(self)
                BoxLayout.setContentsMargins(5,5,5,5)
                BoxLayout.setSpacing(8)

                Middle=HBoxLayout(Addto=BoxLayout)

                MainFrame=FrameBox("MiddleLeft",FrameLayout=Middle,margin=False)
                Main=VBoxLayout(Frame=MainFrame)
                Main.setContentsMargins(5,5,5,5)

                self.map_display = MapWidget(self)

                Main.addWidget(self.map_display)

                self.map_display.mark_location(CityData.Details["latitude"],CityData.Details["longitude"])





class Bottom_section(FrameBox):
        def __init__(self,Layout):
                super().__init__(margin=False)
                Layout.addWidget(self)
                self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
                BoxLayout=VBoxLayout(self)
                BoxLayout.setContentsMargins(15,15,15,15)
                BoxLayout.setSpacing(12)

                # Single unified frame with header and graph
                self.main_frame=FrameBox("MiddleLeft",FrameLayout=BoxLayout,margin=False)
                self.main_layout=VBoxLayout(Frame=self.main_frame)
                self.main_layout.setSpacing(12)
                self.main_layout.setContentsMargins(12,12,12,12)

                # Header section with title and analysis tabs
                HeaderLayout=HBoxLayout(Addto=self.main_layout)
                HeaderLayout.setSpacing(15)
                HeaderLayout.setContentsMargins(0,0,0,0)

                Title=Label("Overview",Addto=HeaderLayout,Name="CityName")
                HeaderLayout.addStretch()
                
                # Analysis options tabs
                AnalysisOptions=HBoxLayout(Addto=HeaderLayout)
                AnalysisOptions.setSpacing(8)
                
                # Create clickable tabs for different analysis metrics
                self.tab_buttons = {}
                self.active_tab = "Temperature"
                self.canvas = None
                
                # Temporary data for each metric
                # timeframe dropdown to switch between hourly and daily graphs
                self.timeframe = "24 hrs"
                self.temp_data = {
                    "Temperature": {
                        "timestamps": list(range(24)),
                        "values": np.array(CityData.Hourly["temperature_2m"][0])
                    },
                    "Humidity": {
                        "timestamps": list(range(24)),
                        "values": np.array(CityData.Hourly["relative_humidity_2m"][0])
                    },
                    "Rainfall": {
                        "timestamps": list(range(24)),
                        "values": np.array(CityData.Hourly["precipitation"][0])
                    }
                }
                # daily summaries for 7‑day view
                self.daily_data = {
                    "Temperature": {
                        "timestamps": list(range(len(CityData.Daily["temperature_2m_max"]))),
                        "values": np.array(CityData.Daily["temperature_2m_max"])
                    },
                    "Humidity": {
                        "timestamps": list(range(len(CityData.Daily["relative_humidity_2m_mean"]))),
                        "values": np.array(CityData.Daily["relative_humidity_2m_mean"])
                    },
                    "Rainfall": {
                        "timestamps": list(range(len(CityData.Daily["precipitation_sum"]))),
                        "values": np.array(CityData.Daily["precipitation_sum"])
                    }
                }
                
                metrics = ["Temperature", "Humidity", "Rainfall"]
                for metric in metrics:
                        btn = QPushButton(metric)
                        btn.setCursor(Qt.CursorShape.PointingHandCursor)
                        btn.setFixedHeight(32)
                        btn.setMinimumWidth(90)
                        btn.setObjectName("AnalysisTab" if metric != "Temperature" else "AnalysisTabActive")
                        btn.clicked.connect(lambda checked, m=metric: self.on_tab_clicked(m))
                        AnalysisOptions.addWidget(btn)
                        self.tab_buttons[metric] = btn

                # add timeframe combo next to tabs
                timeframe_combo = QComboBox()
                timeframe_combo.addItems(["24 hrs", "7 days"])
                timeframe_combo.setFixedHeight(32)
                timeframe_combo.setObjectName("TimeframeCombo")
                timeframe_combo.currentTextChanged.connect(self.on_timeframe_changed)
                AnalysisOptions.addWidget(timeframe_combo)

                
                
                # Graph container directly in main frame
                self.graph_layout=VBoxLayout(Addto=self.main_layout)
                self.graph_layout.setContentsMargins(0,0,0,0)
                self.graph_layout.setSpacing(0)
                self.graph_layout.setStretchFactor(self.graph_layout, 1)
                
                # Create initial graph
                self.create_graph("Temperature")
        
        
        def create_graph(self, metric):
                """Create and display line graph for the selected metric and timeframe"""
                # Remove previous canvas if exists
                if self.canvas is not None:
                        self.graph_layout.removeWidget(self.canvas)
                        self.canvas.deleteLater()
                
                # choose dataset based on timeframe selector
                if self.timeframe == "7 days":
                        data = self.daily_data[metric]
                        # label each tick with weekday name
                        base = Today
                        hours = [(base + dt.timedelta(days=i)).strftime("%a") for i in data["timestamps"]]
                else:
                        data = self.temp_data[metric]
                        hours = [f"{h:02d}:00" for h in data["timestamps"]]
                values = data["values"]
                
                # Convert values to float safely for plotting
                values = np.asarray(values)
                def parse_numeric(v):
                        if isinstance(v, (int, float, np.integer, np.floating)):
                                return float(v)
                        s = str(v).strip()
                        if s in ('-', '', 'None', 'nan', 'NaN'):
                                return np.nan
                        m = re.search(r'[-+]?[0-9]*\.?[0-9]+', s)
                        return float(m.group()) if m else np.nan

                if values.dtype.kind not in 'iufc':
                        values = np.array([parse_numeric(v) for v in values], dtype=float)
                else:
                        values = values.astype(float)
                
                # Create responsive figure - smaller DPI for better scaling
                fig = Figure(figsize=(12, 3), dpi=80)
                fig.patch.set_alpha(0)
                ax = fig.add_subplot(111)
                ax.set_facecolor('none')
                ax.patch.set_alpha(0)
                
                # Plot data without grid using numeric x positions and explicit tick labels
                x = np.arange(len(hours))
                ax.plot(x, values, marker='o', linewidth=2.5, markersize=5, color='#00d4ff', zorder=3)
                ax.fill_between(x, values, alpha=0.25, color='#00d4ff')
                ax.set_xticks(x)
                ax.set_xticklabels(hours)
                
                # Remove grid and spines
                ax.grid(False)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#404040')
                ax.spines['bottom'].set_color('#404040')
                
                # Formatting
                ax.set_title("", fontsize=12, color='#eee', pad=10, fontweight='600')
                ax.set_xlabel("Time", fontsize=8, color='#999')
                
                # Set unit based on metric
                unit = "°C" if metric == "Temperature" else ("%" if metric == "Humidity" else "mm")
                ax.set_ylabel(f"{metric} ({unit})", fontsize=8, color='#999')
                
                # Style ticks
                ax.tick_params(colors='#999', labelsize=7, width=0.5)
                
                # Rotate x-axis labels for better readability
                fig.autofmt_xdate(rotation=45, ha='right')
                
                # Tight layout to prevent label cutoff
                fig.tight_layout(pad=1.0)
                
                # Create canvas with responsive sizing
                self.canvas = FigureCanvas(fig)
                self.canvas.setStyleSheet("background: transparent; border: none;")
                self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.graph_layout.addWidget(self.canvas, stretch=1)
        
        
        def on_tab_clicked(self, metric):
                """Handle tab click and update graph with selected metric data"""
                self.active_tab = metric
                
                # Update button styling
                for tab_name, btn in self.tab_buttons.items():
                        if tab_name == metric:
                                btn.setObjectName("AnalysisTabActive")
                        else:
                                btn.setObjectName("AnalysisTab")
                        btn.style().unpolish(btn)
                        btn.style().polish(btn)
                
                # Update graph with selected metric
                self.create_graph(metric)

        def on_timeframe_changed(self, timeframe):
                """Called when user switches between 24 hrs and 7 days"""
                self.timeframe = timeframe
                # regenerate graph using current metric
                self.create_graph(self.active_tab)


class Right_Region(QWidget):

        def __init__(self):

                super().__init__()
                self.city=MainCity
                self.setContentsMargins(0,0,0,0)

                RightLayout=VBoxLayout(self)
                RightLayout.setContentsMargins(0,0,0,0)
                RightLayout.setSpacing(10)

                self.frame1=HeroSection(Layout=RightLayout)
                self.frame1.setMaximumHeight(80)

                RightMiddleLayout=HBoxLayout(Addto=RightLayout)
                RightMiddleLayout.setSpacing(10)

                frame2_1=Week_data(RightMiddleLayout,self.city)
                frame2_2=ExtraBox(Layout=RightMiddleLayout)
                
                RightMiddleLayout.setStretchFactor(frame2_1, 1)
                RightMiddleLayout.setStretchFactor(frame2_2, 1)

                frame3=Bottom_section(Layout=RightLayout)
                RightLayout.setStretchFactor(frame3, 1)

 

