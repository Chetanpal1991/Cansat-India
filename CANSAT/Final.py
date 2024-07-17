import sys
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                                QVBoxLayout, QLabel, QScrollArea,QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush
from datetime import datetime
from geopy.distance import distance
import numpy as np

file_link = "Add Ons\\trial_data.csv"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telemetry analysis software")
        

        logo_image = QPixmap("Add Ons\\Team Kalpana Logo 1.png").scaledToWidth(130, Qt.TransformationMode.SmoothTransformation)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_image)
        logo_label.setGeometry(10,20,203,250)
       
        background_image = QPixmap("Add Ons\\Team Kalpana Logo background1.png")
        central_widget = QLabel(self)
        self.setCentralWidget(central_widget)
        
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background_image))
        self.setPalette(palette)

        self.label1 = QLabel("TEAM KALPANA", self)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setGeometry(160,108,160,25)
        self.label1.setStyleSheet("font-size: 20px; font-weight: bold; text-decoration: underline;")

        self.label2 = QLabel("TEAM ID: 2022ASI-049", self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setGeometry(150,135,175,50)
        self.label2.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.label3 = QLabel("ALTITUDE :", self)
        self.label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label3.setGeometry(50,225,200,150)
        self.label3.setStyleSheet("font-size: 35px; font-weight: bold;")

        self.label4 = QLabel("PRESSURE :", self)
        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label4.setGeometry(650,225,210,150)
        self.label4.setStyleSheet("font-size: 35px; font-weight: bold;")

        self.label5 = QLabel("RAW TELEMETRY DATA FROM CSV FILE", self)
        self.label5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label5.setGeometry(1020,0,400,100)
        self.label5.setStyleSheet("font-size: 20px; font-weight: bold;font-family: Berlin Sans FB;")

        self.label6 = QLabel("VELOCITY :", self)
        self.label6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label6.setGeometry(1300,225,210,150)
        self.label6.setStyleSheet("font-size: 35px; font-weight: bold;")

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.CSV_Data = CSV_Data(self)
        self.altitude = altitude(self)
        self.altitude_graph = altitude_graph(self)
        self.pressure = pressure(self)
        self.pressure_graph = pressure_graph(self)
        self.velocity = velocity(self)
        self.velocity_graph = velocity_graph(self)


        self.CSV_Data.setParent(self.centralWidget())
        self.altitude.setParent(self.centralWidget())
        self.altitude_graph.setParent(self.centralWidget())
        self.pressure.setParent(self.centralWidget())
        self.pressure_graph.setParent(self.centralWidget())
        self.velocity.setParent(self.centralWidget())
        self.velocity_graph.setParent(self.centralWidget())


        self.CSV_Data.setGeometry(375,75,1525,150)
        self.altitude.setGeometry(300,250,200,100)
        self.altitude_graph.setGeometry(25, 375, 600, 600) 
        self.pressure.setGeometry(900,250,200,100)
        self.pressure_graph.setGeometry(650,375,600,600)
        self.velocity.setGeometry(1550,250,200,100)
        self.velocity_graph.setGeometry(1275,375,600,600)


class CSV_Data(QMainWindow):
    def __init__(self,parent = None):
        super().__init__()
        self.df = pd.read_csv(file_link)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.setStyleSheet(''' 
            border: 1px solid black''')
        
        self.scroll_area = QScrollArea()
        layout.addWidget(self.scroll_area)
        
        self.table_widget = QTableWidget()
        self.scroll_area.setWidget(self.table_widget)
        self.scroll_area.setWidgetResizable(True)  
       
        self.table_widget.setColumnCount(len(self.df.columns))
        self.table_widget.setHorizontalHeaderLabels(self.df.columns)
        
        self.table_widget.resizeColumnsToContents()
        
        self.row_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_next_row)
        self.timer.start(1000)  

    def add_next_row(self):
        if self.row_index < len(self.df):
            
            self.table_widget.insertRow(self.row_index)
            
            row_data = self.df.iloc[self.row_index]
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(self.row_index, j, item)

            self.table_widget.scrollToBottom()

            self.row_index += 1
        else:
            self.timer.stop()


class altitude(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        self.data = pd.read_csv(file_link)

        self.row = 0
        self.rows = ["ALTITUDE"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  

    def displayRow(self):
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['ALTITUDE']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 35px; font-weight: bold;")


class altitude_graph(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.setStyleSheet(''' border: 2px solid black''')

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Altitude', **{'font-size':'20pt' , 'bold':True , 'font-family':'Arial'})
        self.plot_widget.setLabel('bottom', 'Time (s)' , **{'font-size':'20pt' , 'bold':True})

        self.plot_widget.getAxis('left').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))
        self.plot_widget.getAxis('bottom').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))
        
        layout.addWidget(self.plot_widget)

        self.df = pd.read_csv(file_link,usecols=['ALTITUDE'])

        self.time_index = 0
        self.data_index = 0

        self.pen1 = pg.mkPen(color=(255,0,0), width=2 , style=Qt.SolidLine)

        self.timer = QTimer()
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.plot_widget.setLimits(xMin=-1)

    def update_plot(self):
        if self.data_index >= len(self.df):
            self.timer.stop()
            return
        x_data = range(self.data_index + 1)
        y_data = self.df['ALTITUDE'][:self.data_index+1]
        self.plot_widget.plot(x_data, y_data, clear=True , pen = self.pen1 , symbol ="+" , symbolSize=10, symbolBrush="b" )
        self.data_index += 1
        self.time_index += 1


class pressure(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        self.data = pd.read_csv(file_link)

        self.row = 0
        self.rows = ["PRESSURE"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  

    def displayRow(self):
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['PRESSURE']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 35px; font-weight: bold;")


class pressure_graph(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.setStyleSheet(''' border: 2px solid black''')

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'PRESSURE', **{'font-size':'20pt' , 'bold':True , 'font-family':'Arial'})
        self.plot_widget.setLabel('bottom', 'Time (s)' , **{'font-size':'20pt' , 'bold':True})

        self.plot_widget.getAxis('left').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))
        self.plot_widget.getAxis('bottom').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))
        layout.addWidget(self.plot_widget)

        self.df = pd.read_csv(file_link,usecols=['PRESSURE'])

        self.time_index = 0
        self.data_index = 0

        self.pen1 = pg.mkPen(color=(255,0,0), width=2 , style=Qt.SolidLine)

        self.timer = QTimer()
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.plot_widget.setLimits(xMin=-1)

    def update_plot(self):
        if self.data_index >= len(self.df):
            self.timer.stop()
            return

        x_data = range(self.data_index + 1)
        y_data = self.df['PRESSURE'][:self.data_index+1]
        self.plot_widget.plot(x_data, y_data, clear=True , pen = self.pen1 , symbol ="+" , symbolSize=10, symbolBrush="b" )

        self.data_index += 1
        self.time_index += 1


class velocity(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        self.data = pd.read_csv(file_link)

        self.row = 0
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 35px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  

    def displayRow(self):
        if self.row < len(self.data) - 1:
            time1 = self.data.loc[self.row, 'GNSS_TIME']
            time2 = self.data.loc[self.row + 1, 'GNSS_TIME']
            point1 = self.data.loc[self.row, ['GNSS_LATITUDE', 'GNSS_LONGITUDE', 'GNSS_ALTITUDE']].values
            point2 = self.data.loc[self.row + 1, ['GNSS_LATITUDE', 'GNSS_LONGITUDE', 'GNSS_ALTITUDE']].values

            total_distance = self.calculate_total_distance(point1, point2)
            time_difference = self.calculate_time_difference(time1, time2)

            velocity = total_distance / time_difference if time_difference != 0 else 0

            self.label.setText(f"{velocity:.2f} m/s")
            self.row += 1
        else:
            self.timer.stop()

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 35px; font-weight: bold;")

    def calculate_total_distance(self, point1, point2):
        lat1, lon1, alt1 = point1
        lat2, lon2, alt2 = point2

        horizontal_distance = distance((lat1, lon1), (lat2, lon2)).meters
        vertical_distance = abs(alt2 - alt1)

        total_distance = np.sqrt(horizontal_distance**2 + vertical_distance**2)
        return total_distance

    def calculate_time_difference(self, time1, time2):
        time_format = "%H:%M:%S"
        t1 = datetime.strptime(time1, time_format)
        t2 = datetime.strptime(time2, time_format)

        time_difference = (t2 - t1).total_seconds()
        return time_difference
    

class velocity_graph(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        self.data = pd.read_csv(file_link)
        self.row = 0
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Velocity (m/s)', **{'font-size':'20pt' , 'bold':True , 'font-family':'Arial'})
        self.plot_widget.setLabel('bottom', 'Time (s)', **{'font-size':'20pt' , 'bold':True})
        self.layout.addWidget(self.plot_widget)

        self.plot_widget.getAxis('left').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))
        self.plot_widget.getAxis('bottom').setStyle(tickFont=pg.Qt.QtGui.QFont('Arial', 16, pg.Qt.QtGui.QFont.Bold))

        self.times = []
        self.velocities = []

        self.pen1 = pg.mkPen(color=(255,0,0), width=2 , style=Qt.SolidLine)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000) 

        self.start_time = 0

    def update_plot(self):
        if self.row < len(self.data) - 1:
            time1 = self.data.loc[self.row, 'GNSS_TIME']
            time2 = self.data.loc[self.row + 1, 'GNSS_TIME']
            point1 = self.data.loc[self.row, ['GNSS_LATITUDE', 'GNSS_LONGITUDE', 'GNSS_ALTITUDE']].values
            point2 = self.data.loc[self.row + 1, ['GNSS_LATITUDE', 'GNSS_LONGITUDE', 'GNSS_ALTITUDE']].values

            total_distance = self.calculate_total_distance(point1, point2)
            time_difference = self.calculate_time_difference(time1, time2)

            velocity = total_distance / time_difference if time_difference != 0 else 0

            self.times.append(self.start_time)
            self.velocities.append(velocity)
            self.plot_widget.plot(self.times, self.velocities, clear=True, pen = self.pen1 , symbol ="+" , symbolSize=10, symbolBrush="b")

            self.start_time += time_difference
            self.row += 1
        else:
            self.timer.stop()

    def calculate_total_distance(self, point1, point2):
        lat1, lon1, alt1 = point1
        lat2, lon2, alt2 = point2
        horizontal_distance = distance((lat1, lon1), (lat2, lon2)).meters
        vertical_distance = abs(alt2 - alt1)

        total_distance = np.sqrt(horizontal_distance**2 + vertical_distance**2)
        return total_distance
    
    def calculate_time_difference(self, time1, time2):
        time_format = "%H:%M:%S"
        t1 = datetime.strptime(time1, time_format)
        t2 = datetime.strptime(time2, time_format)

        time_difference = (t2 - t1).total_seconds()
        return time_difference

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("Add Ons\\Team Kalpana Logo.png"))

    mainwindow = MainWindow()
    mainwindow.showMaximized()
    sys.exit(app.exec())