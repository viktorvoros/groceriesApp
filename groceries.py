import kivy
from kivy.app import App
from kivy.app import runTouchApp
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


class WindowManager(ScreenManager):
    pass

class MainWindow(BoxLayout):
    pass

class HomeWindow(Screen):
    homeBtn = OptionProperty('normal')
    homeBtn = 'down'
    def listBtn(self, textinput):
        self.listGrid.add_widget(Label(text=self.list.text, color=(0,0.4,0,1),bold=True,text_size = [360, 30] , halign="left",valign="middle"))

    def listBtnRelease(self):
        self.list.text = "New list..."

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
        self.listContainer.add_widget(CheckBox(size_hint_x=None, width=30 ))
        self.listContainer.add_widget(ToggleButton(text=self.item.text, text_size = [360, 30] , halign="left",valign="middle"))
        # print(self.listContainer.children)
        self.addBtnRelease()
        # print(self.size)
    def addBtnRelease(self):
        self.item.text = "Add an item..."

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

class todoApp(App):
    def build(self):
        Window.size = (400, 800)
        return MainWindow()


if __name__ =="__main__":
    todoApp().run()
