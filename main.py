from PyQt5 import QtWidgets
from routeplan import Ui_MainWindow
import sys
import json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt





class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Configure window
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Add the map widget to the empty 'frame_plot' frame
        self.map = MapCanvas(self, self.ui.frame_plot.width()/10, self.ui.frame_plot.height()/10)
        self.ui.frame_plot.layout().addWidget(self.map)

        # Connect signals and slots
        self.ui.button_plot.clicked.connect(lambda: self.map.click(self.ui))


class MapCanvas(FigureCanvas):
    """Matplotlib map-plot widget"""

    def __init__(self, parent=None, width=20, height=20):
        # Init the plot widget
        self.fig = plt.figure(figsize=(width, height))     
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def click(self, ui):
        problem_id = int(ui.lineEdit.text())
        path_choice = int(ui.lineEdit_2.text())
        if problem_id >= 1 and problem_id <= 12 and path_choice >= 0 and path_choice <= 1:
            self.plot(problem_id, path_choice)
    
    def plot(self, problem_id, path_choice):
        with open(f"./data/Problem_{problem_id}.json",'r') as load_f:
            problem = json.load(load_f)

        map = problem['Map']
        start_x = problem['START_x']
        start_y = problem['START_y']
        goal_x = problem['GOAL_x']
        goal_y = problem['GOAL_y']
        red_areas = []
        if 'Red_areas' in problem.keys():
            red_areas = problem['Red_areas']

        yellow_areas = []
        if 'Yellow_areas' in problem.keys():
            yellow_areas = problem['Yellow_areas']


        obstacle_x = []
        obstacle_y = []
        dim_x = len(map[0])
        dim_y = len(map)
        for i in range(dim_y):
            for j in range(dim_x):
                if map[i][j] == 1:
                    obstacle_x.append(j + 1)
                    obstacle_y.append(i + 1)
        yellow_areas_x = []
        yellow_areas_y = []
        for i in range(len(yellow_areas)):
            yellow_areas_x.append(yellow_areas[i][0])
            yellow_areas_y.append(yellow_areas[i][1])

        red_areas_x = []
        red_areas_y = []
        for i in range(len(red_areas)):
            red_areas_x.append(red_areas[i][0])
            red_areas_y.append(red_areas[i][1])
            

        id_result = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII','XIII']
        path_x = []
        path_y = []
        first = True
        for line in open(f"./output/Table {id_result[problem_id]}.txt"): 
            line = line.split()
            if first:
                first = False
                continue
            if path_choice == 1:
                path_id = 0
            else :
                path_id = -1
            x, y = int(line[path_id * 2]), int(line[path_id * 2 + 1])
            if x == 0 or y == 0:
                continue
            path_x.append(x)
            path_y.append(y)

        plt.cla()
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        size = 10
        plt.grid(True)  
        plt.plot(path_x,path_y,linewidth=2)
        plt.scatter(start_x, start_y, s=size,c='b',marker='s')
        plt.scatter(obstacle_x, obstacle_y,s=size,c='k',marker='s')
        plt.scatter(goal_x, goal_y,s=size,c='g',marker='s')
        plt.scatter(yellow_areas_x, yellow_areas_y,s=size,c='k',marker='s')
        plt.scatter(red_areas_x, red_areas_y,s=size,c='r',marker='s')
        self.draw()
        self.flush_events()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())
