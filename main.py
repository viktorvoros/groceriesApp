import kivy
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import ILeftBodyTouch,IRightBodyTouch, OneLineAvatarIconListItem
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.carousel import Carousel
from ScreenManagementHome import *
from HomeWindow import *
from ListWindow import *
from ChartWindow import *
from CalendarWindow import *


class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_screen = NumericProperty()
    list_number = StringProperty()
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()

class SwipeButton(Carousel):
    item_name = StringProperty()
    item_category = StringProperty()
    item_index = NumericProperty()
    item_quantity = StringProperty()
    item_price = StringProperty()
    item_note = StringProperty()
    item_image = StringProperty()
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(SwipeButton, self).__init__(**kwargs)

class ListItem(BoxLayout):
    '''Custom list item.'''
    item_name = StringProperty()
    item_category = StringProperty()
    item_index = NumericProperty()
    item_quantity = StringProperty()
    item_price = StringProperty()
    item_note = StringProperty()
    item_image = StringProperty()
    icon = StringProperty("food")

class CategoryIcon(MDIconButton, IRightBodyTouch):
    item_category = StringProperty()
    def __init__(self, **kwargs):
        super(CategoryIcon, self).__init__(**kwargs)
        if self.item_category == 'Dairy':
            icon = StringProperty("food")
        else:
            icon = StringProperty("android")

class CounterLabel(IRightBodyTouch, MDLabel):
    list_number = NumericProperty()

class ItemCounterLabel(IRightBodyTouch, MDLabel):
    item_number = NumericProperty()
    item_number = 0
    item_number = str(item_number)

class IconButtonRight(IRightBodyTouch, MDIconButton):
    pass

class IconButtonLeft(ILeftBodyTouch, MDIconButton):
    pass

class MainWindow(Screen):
    pass

class RecipesWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

# kv = Builder.load_file("groceriesApp.kv")
class groceriesApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return MainWindow()


if __name__ =="__main__":
    groceriesApp().run()
