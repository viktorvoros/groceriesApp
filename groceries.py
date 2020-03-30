import kivy
from kivy.app import App
from kivy.app import runTouchApp
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List for shopping list'''

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Items list.'''
    icon = StringProperty("food")

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''

class WindowManager(ScreenManager):
    pass

class MainWindow(BoxLayout):
    pass

class HomeWindow(Screen):
    homeBtn = OptionProperty('normal')
    homeBtn = 'down'
    def listBtn(self, textinput):
        self.listGrid.add_widget(ListItemWithCounter(text=self.list.text))

    def listBtnRelease(self):
        self.list.text = ""

class RecipesWindow(Screen):
    pass

class ChartWindow(Screen):
    pass

class CalendarWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class CatalogueWindow(Screen):
    pass

class ListWindow(Screen):

    # def __init__(self,**kwargs):
    #     super(ListWindow, self).__init__(**kwargs)
    item = ObjectProperty(None)
    listContainer = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ListWindow, self).__init__(**kwargs)

    def addBtn(self, textinput):
        # self.listContainer.add_widget(ToggleButton(text=self.item.text))
        self.listContainer.add_widget(ListItemWithCheckbox(text=self.item.text))
        # print(self.listContainer.children)
        self.addBtnRelease()
        # print(self.size)
    def addBtnRelease(self):
        self.item.text = ""

    def catalogueBtn(self):
        pass

    def emptyBtn(self):
        for child in [child for child in self.listContainer.children]:
            self.listContainer.remove_widget(child)

    def chartBtn(self):
        show = FloatLayout()
        popupWindow = Popup(title="Groceries chart", content=show, size_hint = (None,None), size=(400,400))
        popupWindow.open()

kv = Builder.load_file("groceries.kv")

class todoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        Window.size = (400, 800)
        return MainWindow()


if __name__ =="__main__":
    todoApp().run()
