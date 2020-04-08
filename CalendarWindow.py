import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker


class CalendarWindow(Screen, BoxLayout):
    def __init__(self,**kwargs):
        super(CalendarWindow,self).__init__(**kwargs)
        self.add_widget(MDDatePicker(callback=self.get_date))
        # time_dialog.open()

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''
