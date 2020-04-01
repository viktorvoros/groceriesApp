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
    list_number = StringProperty()

class ChartWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    pass

class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_number = StringProperty()
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()
    # print(list_number)

class ListItem(OneLineAvatarIconListItem):
    '''Custom list item.'''
    list_title = StringProperty()
    list_content = StringProperty()
    list_index = NumericProperty()

    icon = StringProperty("android")

class CounterLabel(IRightBodyTouch, MDLabel):
    pass
    # list_number = NumericProperty()
    # list_number =

class ItemCounterLabel(IRightBodyTouch, MDLabel):
    item_number = NumericProperty()
    item_number = 0
    item_number = str(item_number)

class IconButtonRight(IRightBodyTouch, MDIconButton):
    pass

class IconButtonLeft(ILeftBodyTouch, MDIconButton):
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''

class Tab(FloatLayout, MDTabsBase):
    pass

class MainWindow(Screen):

    pass

class HomeWindow(Screen):

    data = ListProperty()
    # list_number = StringProperty()

    def _get_data_for_widgets(self):
        return [{
            'list_index': index,
            'list_content': item['content'],
            'list_title': item['title'],
            'list_number': item['number']}
            for index, item in enumerate(self.data)]

    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

    def clearTxt(self, TextInput):
        self.list.text = ''

class ListWindow(Screen, MDApp):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    list_number = StringProperty()
    data = ListProperty()


    def _get_data_for_items(self):
        return [{
            'list_index': index,
            'list_content': item['content'],
            'list_title': item['title'],
            'list_number': item['number']}
            for index, item in enumerate(self.data)]

    data_for_items = AliasProperty(_get_data_for_items, bind=['data'])
    def __init__(self,**kwargs):
        super(ListWindow, self).__init__(**kwargs)
        self.root = ScreenManagementHome()
        self.load_items()
        self.list_number = str(len(self.data))


    def add_item(self, textinput):
        # self.load_items()
        self.data.append({'title': textinput, 'content': '', 'number': ''})
        list_index = len(self.data) - 1
        self.list_number = str(len(self.data))
        # numberOfItems = str(int(self.list_number) + 1)
        # self.data['number'] = numberOfItems
        # self.refresh_items()
        # self.list.text = ''
        # self.edit_list(list_index)
        # print(len(self.data))
        self.save_items()

    def edit_list(self, list_index):
        list = self.data[list_index]
        name = 'ch{}'.format(list_index)
        self.list_number = str(len(self.data))

        if self.parent.has_screen(name):
            self.parent.remove_widget(self.sm.get_screen(name))

        view = ChartWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.parent.add_widget(view)
        # self.transition.direction = 'left'
        self.parent.current = view.name

    def load_items(self):
        if not exists(self.items_fn):
            return
        with open(self.items_fn) as fd:
            data = json.load(fd)
        self.data = data
        self.list_number = str(len(self.data))

    def clearTxt(self, TextInput):
        self.item.text = ''

    def del_item(self, list_index):
        del self.data[list_index]
        self.save_items()
        self.refresh_items()

    def empty_list(self, list_index):
        # self.data[list_index] = []
        # self.refresh_items()
        # self.save_items()
        print(self.data)
        del self.data[list_index]
        print(self.data)
        self.save_items()
        self.refresh_items()

    def save_items(self):
        with open(self.items_fn, 'w') as fd:
            json.dump(self.data, fd)

    def refresh_items(self):
        data = self.data
        self.data = []
        self.data = data
        self.list_number = str(len(self.data))

    def refresh_data(self, list_index, list_number):
        data = self.data[list_index]
        data['number'] = list_number
        self.data[list_index] = []
        self.data[list_index] = data
    @property
    def items_fn(self):
        return join(self.user_data_dir, 'items.json')

    def goBack(self):
        self.parent.current = 'HomeWindow'
        self.parent.transition.direction = "right"

    def addItem(self, textinput):
        self.item = ListItemWithCheckbox(text=self.itemText.text)
        # self.item.bind(on_active=self.rmvItem)
        self.ids.itemGrid.add_widget(self.item)
        self.itemText.text = ''
        # print(self.item.children)

    def rmvItem(self, *args, **kwargs):
        self.ids.itemGrid.remove_widget(self.item)

class RecipesWindow(Screen):
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
        self.items = ListWindow()
        self.load_lists()
        Window.size = (400, 800)
        self.transition = SlideTransition()
        root = ScreenManagementHome(transition=self.transition)
        root.add_widget(self.lists)
        return root

    def add_list(self, textinput, number):
        self.lists.data.append({'title': textinput, 'content': '', 'number': number})
        list_index = len(self.lists.data) - 1
        self.refresh_lists()
        # self.list.text = ''
        # self.edit_list(list_index)

    def edit_list(self, list_index, list_number):
        list = self.lists.data[list_index]
        print(list)
        name = 'list{}'.format(list_index)

        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.root.add_widget(view)
        self.transition.direction = 'left'
        numberOfItems = str(int(view.list_number) + 1)
        self.lists.list_number = numberOfItems
        self.lists.data[list_index]['number'] = str(view.list_number)
        self.root.current = view.name
        self.refresh_lists()

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

    def refresh_data(self, list_index, list_number):
        data = self.lists.data[list_index]
        data['number'] = list_number
        self.lists.data[list_index] = []
        self.lists.data[list_index] = data
        self.save_lists()

    def go_lists(self):
        self.transition.direction = 'right'
        self.root.current = 'lists'

    def del_list(self, list_index):
        list = self.lists.data[list_index]
        name = 'list{}'.format(list_index)
        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        # print(view.data)
        view.empty_list(list_index)
        del self.lists.data[list_index]
        self.save_lists()
        self.refresh_lists()
        self.go_lists()

    @property
    def lists_fn(self):
        return join(self.user_data_dir, 'lists.json')

if __name__ =="__main__":
    groceriesApp().run()
