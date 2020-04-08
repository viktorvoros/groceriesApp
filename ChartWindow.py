import kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, AliasProperty
import matplotlib
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use
from matplotlib.figure import Figure
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import json
from os.path import join, exists
from kivy.clock import Clock

class ChartWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    stat = ListProperty()
    spent = 0.0


    def __init__(self, **kwargs):
        global canvas
        super(ChartWindow, self).__init__(**kwargs)

        self.plotStat()

        self.fig, self.ax1 = plt.subplots()

        plt.bar(1,self.spent)



        Clock.schedule_once(self._do_setup)

    def _do_setup(self, *l):
        self.pl()

    def pl(self):

        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.ids.box.add_widget(canvas)
        canvas.draw()

    def updatePlot(self):
        # self.plotStat()
        plt.clf()
        # plt.bar(1, self.spent)
        # canvas.draw()
        # fig, ax = plt.subplots()
        # plt.bar('Mar', self.spent)
        # self.canvas.draw

    def loadStat(self):
        if not exists('data/stat.json'.format(self.name)):
            return
        with open('data/stat.json'.format(self.name)) as fd:
            stat = json.load(fd)
        self.stat = stat

    # def changeLabel(self):
    #     self.ids.lab.text = 'pressed'
    #     self.ch.ids.gr.add_widget(Button(text='added'))

    def plotStat(self):
        self.loadStat()
        nam = []
        for i in range(0,len(self.stat)):
            nam.append(float(self.stat[i]['quantity'])* float(self.stat[i]['price']))
        print(sum(nam))
        self.spent =sum(nam)
        # fig, ax = plt.subplots()
        # plt.bar(1, self.spent)
        # canvas = fig.canvas
