import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

class ScreenManagementHome(ScreenManager):
    # contains HomeWindow and ListWindow
    pass

class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List for shopping list'''


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''



class MainWindow(Screen):
    #contains the bottom navigation and all the windows
    pass

class HomeWindow(Screen):
    def __init__(self,**kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.nb = 0
        # screenmanager = ObjectProperty()
        # listGrid = ObjectProperty(None)
        # print(self.ids)
    def listBtn(self, TextInput):
        # self.listItem = ObjectProperty(None)
        self.listItem = ListItemWithCounter(text=self.list.text)
        self.ids.listGrid.add_widget(self.listItem)
        self.list.text = ''
        # self.listItem.id = str(self.list.text)
        self.listItem.bind(on_release= self.rmv)
        # listItem.on_press(self.sm.current.s)
        # print(self.ids.sm)
        # s = Screen(name=self.list.text)
        # s.add_widget(ListWindow())
        # self.ids.add_widget(listItem)
        # self.ids.sm.add_widget(s)
        # print(self.id)
        self.nb +=1
        # print(self.ids)
    def rmv(self, *args, **kwargs):
        print('yay')
        self.parent.current='ListWindow'
        self.parent.transition.direction = "left"

class ListWindow(Screen):
    def goBack(self):
        self.parent.current = 'HomeWindow'
        self.parent.transition.direction = "right"

    def addItem(self, textinput):
        self.item = ListItemWithCheckbox(text=self.itemText.text)
        # self.item.bind(on_active=self.rmvItem)
        self.ids.itemGrid.add_widget(self.item)
        self.itemText.text = ''
        print(self.item.children)

    def rmvItem(self, *args, **kwargs):
        self.ids.itemGrid.remove_widget(self.item)

class RecipesWindow(Screen):
    pass

class ChartWindow(Screen):
    pass

class CalendarWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

# kv = Builder.load_file("groceriesApp.kv")

class groceriesApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        Window.size = (400, 800)
        # return my_screenmanager
        return MainWindow()

if __name__ =="__main__":
    groceriesApp().run()
