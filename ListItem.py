import kivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

class ListItem(BoxLayout):
    '''Custom list item.'''
    item_name = StringProperty()
    item_category = StringProperty()
    item_index = NumericProperty()
    item_quantity = StringProperty()
    item_price = StringProperty()
    item_note = StringProperty()
    item_image = StringProperty()
    item_checked = StringProperty()
    icon = StringProperty("food")

class ItemPopup(Popup):
    item_name = StringProperty()
    item_category = StringProperty()
    item_index = NumericProperty()
    item_quantity = StringProperty()
    item_price = StringProperty()
    item_note = StringProperty()
    item_image = StringProperty()
    def __init__(self, **kwargs):
        self.caller = kwargs.pop('caller')
        super(ItemPopup, self).__init__(**kwargs)

    def on_open(self):
        self.background = 'transp.png'
