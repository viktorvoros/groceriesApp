import kivy
from kivy.uix.screenmanager import ScreenManager

class ScreenManagementHome(ScreenManager):
    transition = 'left'

    def go_lists(self):
        self.transition.direction = 'right'
        self.current = 'lists'
