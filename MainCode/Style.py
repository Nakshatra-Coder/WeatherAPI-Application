from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


def ApplyStyles(window):
        """Apply application styles to the given main window.

        Usage: call ApplyStyles(window) after the window is created.
        """
        base_font = QFont("Poppins Medium", 10)
        app = QApplication.instance()
        if app is not None:
                app.setFont(base_font)

        dark = getattr(window, 'Dark_mode', True)

        palette_bg = "#0b1226" if dark else "#f4f6fb"
        card_bg = "#141a2e" if dark else "#ffffff"
        text_primary = "#e6e8ee" if dark else "#1a1a1a"
        text_muted = "#9aa1af" if dark else "#666"
        accent = "#7c9cff"
        gradient_top = "#303033"
        gradient_bottom = "#191B1D"
        gradient_top_2 = "#0EBAFB"
        gradient_bottom_2 = "#0668AB"

        base_back = "#313439"
        base_back_hover = "#47494B"
        base_border = "#707070"

        window.setStyleSheet(f"""
QMainWindow {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {gradient_top}, stop:1 {gradient_bottom});
}}

#TopLevel{{
        background: #3C3D40;
}}

#DisplayedCity {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {gradient_top_2}, stop:1 {gradient_bottom_2});
        border: 1px solid {base_border};
        border-radius: 48px;
}}

#Scroll{{
        background:transparent;
}}
QScrollArea{{
        background:transparent;
}}
#BaseBoxes {{
        background:{base_back};
        border: 2px solid #404040;
        border-radius: 36px;
}}
#BaseBoxes1 {{
        background:{base_back};
        border: 2px solid #404040;
        border-radius: 36px;
}}
#BaseBoxes1:hover {{
        background: {base_back_hover};
        border: 2px solid #404040;
        border-radius: 36px;
}}
QLabel {{
        color: #eee;
        text-align: center;
        font-weight: 600;
        font-family: 'Poppins';
}}
#Time {{
        font-size: 15px;
}}
#WeatherIcon-Larger {{
        font-size: 120px;
}}
#WeatherIcon {{
        font-size: 90px;
}}
#WeatherIcon-Smaller {{
        font-size: 50px;
}}
#Large-Text {{
        font-size: 70px;
        color: #eee;
}}
#CityName {{
        font-size: 18px;
}}
#OtherCityTemp {{
        font-size: 32px;
}}
#AddCityBox {{
        border: 5px dashed #404040;
        border-radius: 36px;
}}
#AddCityImageBox {{
        width: 40px;
        background: {base_back};
        border: 2px solid #404040;
        border-radius: 20px;
}}
#SearchArea {{
        border-radius: 28px;
        padding: 0px 20px;
        border: 1px solid {base_border};
        background: {base_back};
}}
#SearchTab {{
        background: {base_back};
        outline: none;
        border: none;
        color: #ccc;
        font-family: Poppins;
        font-size: 1.5rem;
}}
#ModeToggle {{
        background: {base_back};
        padding: 20px;
        color: #eee;
        border-radius: 24px;
        border: 1px solid {base_border};
}}
#NotificationArea {{
        background: {base_back};
        border: 1px solid {base_border};
        padding: 20px;
        border-radius: 24px;
}}
#AccountImage {{
        border: 1px solid {base_border};
}}
#MiddleLeft,#MiddleRight,#Footer {{
        background: {base_back};
        border-radius: 32px;
        border: 1px solid {base_border};
}}
#MiddleLeft {{
        padding: 10px;
}}
#Footer {{
        padding: 20px;
}}
#FooterOptions {{
        background: #444;
        border: 3px solid {base_border};
        border-radius: 20px;
}}
#Option {{
        padding:0 12px;
}}
#GraphFrame {{
        background: {base_back};
        border-radius: 32px;
        border: 1px solid {base_border};
        padding: 15px;
}}
#AnalysisTab {{
        background: #2a2a2a;
        color: #999;
        border: 1px solid #404040;
        border-radius: 8px;
        padding: 5px 15px;
        font-weight: 600;
}}
#AnalysisTab:hover {{
        background: #333333;
}}
#AnalysisTabActive {{
        background: #00d4ff;
        color: #000;
        border: 1px solid #00d4ff;
        border-radius: 8px;
        padding: 5px 15px;
        font-weight: 600;
}}
QComboBox#TimeframeCombo {{
        background: #333;
        color: #eee;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 4px 8px;
}}
QComboBox#TimeframeCombo::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 1px;
        border-left-color: #555;
        border-left-style: solid;)
}}
#AddCityBox{{
        border: 5px dashed {'#404040'};
        border-radius: 36px;
}}
#AddImage{{
        width: 40px;
        background: {base_back};
        border: 2px solid {'#404040'};
        border-radius: 20px;
}}
#Button2{{
        background:#CECECE;
        border:none;
        color:#2B2B2B;
        padding:12px 16px 12px 16px;
}}
#Button2::hover{{
        background: {"#B2B2B2"};
}}


""")