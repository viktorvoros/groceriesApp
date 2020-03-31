import json
from os.path import join, exists
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import ILeftBodyTouch,IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, AliasProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.checkbox import CheckBox

class ScreenManagementHome(ScreenManager):
    # contains HomeWindow and ListWindow
    pass


class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()
    # list_number = StringProperty()
    # list_number = 'hello'

class CounterLabel(IRightBodyTouch, MDLabel):
    list_number = StringProperty()
    list_number = '0'

class ItemCounterLabel(IRightBodyTouch, MDLabel):
    item_number = NumericProperty()
    item_number = 0
    item_number = str(item_number)

class IconButtonRight(IRightBodyTouch, MDIconButton):
    pass

class IconButtonLeft(ILeftBodyTouch, MDIconButton):
    pass

class ListItem(OneLineAvatarIconListItem):
    '''Custom list item.'''
    list_title = StringProperty()
    icon = StringProperty("android")


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''

class Tab(FloatLayout, MDTabsBase):
    pass

class MainWindow(Screen):

    pass

class HomeWindow(Screen):

    data = ListProperty()

    def _get_data_for_widgets(self):
        return [{
            'list_index': index,
            'list_content': item['content'],
            'list_title': item['title']}
            for index, item in enumerate(self.data)]

    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

    def clearTxt(self, TextInput):
        self.list.text = ''

class ListWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()

    data = ListProperty()

    def _get_data_for_items(self):
        return [{
            'list_index': index,
            'list_content': item['content'],
            'list_title': item['title']}
            for index, item in enumerate(self.data)]

    data_for_items = AliasProperty(_get_data_for_items, bind=['data'])

    def add_item(self, textinput):
        self.data.append({'title': textinput, 'content': ''})
        list_index = len(self.data) - 1
        # self.list.text = ''
        # self.edit_list(list_index)
        print(list_index)

    def clearTxt(self, TextInput):
        self.item.text = ''

    def del_item(self, list_index):
        del self.data[list_index]
        self.save_items()
        self.refresh_items()

    def save_items(self):
        with open(self.items_fn, 'w') as fd:
            json.dump(self.data, fd)

    def refresh_items(self):
        data = self.data
        self.data = []
        self.data = data

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
        # self.theme_cls.primary_palette = "Green"
        self.lists = HomeWindow(name='lists')
        self.load_lists()
        Window.size = (400, 800)
        self.transition = SlideTransition()
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.lists)
        root.add_widget(ChartWindow())
        return root

    def add_list(self, textinput):
        self.lists.data.append({'title': textinput, 'content': ''})
        list_index = len(self.lists.data) - 1
        # self.list.text = ''
        # self.edit_list(list_index)
        print(list_index)

    def edit_list(self, list_index):
        list = self.lists.data[list_index]
        name = 'list{}'.format(list_index)

        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name

    def set_list_content(self, list_index, list_content):
        self.lists.data[list_index]['content'] = list_content
        data = self.lists.data
        self.lists.data = []
        self.lists.data = data
        self.save_lists()
        self.refresh_lists()

    def set_list_title(self, list_index, list_title):
        self.lists.data[list_index]['title'] = list_title
        self.save_lists()
        self.refresh_lists()

    def save_lists(self):
        with open(self.lists_fn, 'w') as fd:
            json.dump(self.lists.data, fd)

    def load_lists(self):
        if not exists(self.lists_fn):
            return
        with open(self.lists_fn) as fd:
            data = json.load(fd)
        self.lists.data = data

    def refresh_lists(self):
        data = self.lists.data
        self.lists.data = []
        self.lists.data = data

    def go_lists(self):
        self.transition.direction = 'right'
        self.root.current = 'lists'

    def del_list(self, list_index):
        del self.lists.data[list_index]
        self.save_lists()
        self.refresh_lists()
        self.go_lists()

    

    @property
    def lists_fn(self):
        return join(self.user_data_dir, 'lists.json')

if __name__ =="__main__":
    groceriesApp().run()
