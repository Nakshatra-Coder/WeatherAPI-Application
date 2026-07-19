from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor,QPixmap
import datetime as dt
import pytz
import os

Today=dt.datetime.now()


LEFT=Qt.AlignmentFlag.AlignLeft
RIGHT=Qt.AlignmentFlag.AlignRight
CENTER=Qt.AlignmentFlag.AlignCenter
TOP=Qt.AlignmentFlag.AlignTop
BOTTOM=Qt.AlignmentFlag.AlignBottom

TOP_LEFT=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
TOP_RIGHT=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight


def PATH(name: str) -> str:   # ONLY FOR FILE PATH

    current_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(current_dir,"DataStorage",name)


class HBoxLayout(QHBoxLayout):
        def __init__(self,Frame=None, Addto=None,stretch=None, *args, **kwargs):
                if Frame is not None:
                        super().__init__(Frame,*args,**kwargs)
                else:
                        super().__init__(*args,**kwargs)
                self.setSpacing(30) 
                # Handle both QWidget and QLayout
                if Addto is not None: 
                        if isinstance(Addto, QWidget): 
                                Addto.setLayout(self) 
                        elif isinstance(Addto, QHBoxLayout) or isinstance(Addto, QVBoxLayout) or hasattr(Addto, "addLayout"): 
                                Addto.addLayout(self)

        def setSpacing(self, spacing):
                return super().setSpacing(spacing)

class VBoxLayout(QVBoxLayout):
        def __init__(self,Frame=None,Addto=None,*args,**kwargs):
                if Frame is not None:
                        super().__init__(Frame,*args,**kwargs)
                else:
                        super().__init__(*args,**kwargs)
                self.setSpacing(10)
                if Addto is not None: 
                        if isinstance(Addto, QWidget): 
                                Addto.setLayout(self) 
                        elif isinstance(Addto, QHBoxLayout) or isinstance(Addto, QVBoxLayout) or hasattr(Addto, "addLayout"): 
                                Addto.addLayout(self)

        def addWidget(self, a0, stretch = 1):
               return super().addWidget(a0, stretch)

        def setSpacing(self, spacing):
                return super().setSpacing(spacing)


                



class FrameBox(QFrame):

        clicked=pyqtSignal()

        def __init__(self,Name=None,FrameLayout=None,height=None,margin=True):
                super().__init__()
                if FrameLayout!=None:FrameLayout.addWidget(self)
                if Name!=None:self.setObjectName(Name)

                shadow=QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setOffset(3,3)
                shadow.setColor(QColor(0,0,0,80))

                self.setGraphicsEffect(shadow)

                if margin==True:self.setContentsMargins(8,16,8,16)

        def mousePressEvent(self, ev):
               self.clicked.emit()
               super().mousePressEvent(ev)

        def setMinimumHeight(self, minh):
                return super().setMinimumHeight(minh)
        
        def setMaximumHeight(self, maxh):
                return super().setMaximumHeight(maxh)
        
        def setFixedHeight(self, h):
                return super().setFixedHeight(h)

        def setMinimumWidth(self, minw):
                return super().setMinimumWidth(minw)
        
        def setMaximumWidth(self, maxw):
                return super().setMaximumWidth(maxw)
        
        def setFixedWidth(self, w):
                return super().setFixedWidth(w)
                

class Label(QLabel):

        clicked=pyqtSignal()

        def __init__(self,Text,Addto=None,Name=None,Alignment=None,*args,**kwargs):
                super().__init__(Text)
                if Addto!=None:
                        if isinstance(Addto, list):
                                Addto[0].addWidget(self,Addto[1],Addto[2])
                        else:
                                Addto.addWidget(self)
                if Name!=None:self.setObjectName(Name)
                if Alignment!=None:self.setAlignment(Alignment)

                

        def mousePressEvent(self, ev):
               self.clicked.emit()
               super().mousePressEvent(ev)

        def setVisible(self, visible):
               return super().setVisible(visible)


class Image(QLabel):

        def __init__(self,Name=None,IAddress="",Layout=None,Scale=[20,20],Alignment=CENTER):
                
                super().__init__()
                if Name is not None:self.setObjectName(Name)
                if Layout is not None:Layout.addWidget(self)
                pixmap=QPixmap(IAddress)
                scaled_pixmap=pixmap.scaled(Scale[0],Scale[1],Qt.AspectRatioMode.KeepAspectRatio)
                self.setPixmap(scaled_pixmap)
                self.setAlignment(Alignment)


class TimeZone:
    def __init__(self,zone):
           tz=pytz.timezone(zone)
           self.current_time=dt.datetime.now(tz)

           

class Weather:
    WEATHER_MAP_DAY = {
        0: ("☀️", "Sunny"),
        1: ("🌤️", "Mostly sunny"),
        2: ("⛅", "Partly cloudy"),
        3: ("☁️", "Cloudy"),
        45: ("🌫️", "Fog"),
        48: ("🌫️", "Fog"),
        51: ("🌦️", "Light drizzle"),
        53: ("🌦️", "Drizzle"),
        55: ("🌧️", "Heavy drizzle"),
        61: ("🌦️", "Light rain"),
        63: ("🌧️", "Rain"),
        65: ("🌧️", "Heavy rain"),
        71: ("🌨️", "Light snow"),
        73: ("🌨️", "Snow"),
        75: ("❄️", "Heavy snow"),
        77: ("❄️", "Snow grains"),
        80: ("🌦️", "Showers"),
        81: ("🌧️", "Rain showers"),
        82: ("🌧️", "Heavy showers"),
        85: ("🌨️", "Snow showers"),
        86: ("❄️", "Heavy snow showers"),
        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Storm with hail"),
        99: ("⛈️", "Severe storm"),
    }

    WEATHER_NIGHT_OVERRIDES = {
        0: ("🌙", "Clear night"),
        1: ("🌙", "Mostly clear night"),
        2: ("☁️", "Partly cloudy night"),
    }

    @classmethod
    def interpret(cls, code, city=None):
        # Simple day/night rule: 6 AM–6 PM is day, else night
        if city==None:
               hour = Today.hour
               is_night = not (6 <= hour < 19)
        
        else:
               current_time=TimeZone(city)
               is_night=not (6 <= current_time.current_time.hour < 19)

        try:
            if is_night and code in cls.WEATHER_NIGHT_OVERRIDES:
                result = cls.WEATHER_NIGHT_OVERRIDES.get(code, ("❓", "Unknown"))
            else:
                result = cls.WEATHER_MAP_DAY.get(code, ("❓", "Unknown"))
        except:
            result = ("❓", "Unknown")
        finally:
            return result



"""
Can we just add setMaximum and setMinimum height and width of the frames much easily.
Can we make the frame argument feature turn on while using the addto argument, we can use interface for it may be.
"""