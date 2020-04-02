import json
from os.path import join, exists
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, AliasProperty
from kivy.uix.button import Button

class ScreenManagementHome(ScreenManager):
    def go_lists(self):
        # self.transition.direction = 'right'
        self.current = 'lists'
    # contains HomeWindow and ListWindow
    # def __init__(self,**kwargs):
    #     super(ScreenManagementHome, HomeWindow, self).__init__(**kwargs)
    #     self.add_widget(HomeWindow(name='lists'))
    pass

class ListWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    def edit_list(self, list_index):
        list = self.data[list_index]
        name = 'list{}'.format(list_index)

        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.root.add_widget(view)
        # self.transition.direction = 'left'
        self.root.current = view.name

    def set_list_content(self, list_index, list_content):
        self.data[list_index]['content'] = list_content
        data = self.data
        self.data = []
        self.data = data
        self.save_lists()
        self.refresh_lists()

    def set_list_title(self, list_index, list_title):
        self.data[list_index]['title'] = list_title
        self.save_lists()
        self.refresh_lists()
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

class ChartWindow(Screen):
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
    def __init__(self,**kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # self.sm = ScreenManagementHome()

    def add_list(self, textinput):
        self.data.append({'title': textinput, 'content': ''})
        list_index = len(self.data) - 1
        # self.edit_list(list_index)
        print(list_index)

    def edit_list(self, list_index):
        list = self.data[list_index]
        name = 'list{}'.format(list_index)

        if self.parent.has_screen(name):
            self.parent.remove_widget(self.parent.get_screen(name))

        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.parent.add_widget(view)
        # self.transition.direction = 'left'
        self.parent.current = view.name

    def set_list_content(self, list_index, list_content):
        self.data[list_index]['content'] = list_content
        data = self.data
        self.data = []
        self.data = data
        self.save_lists()
        self.refresh_lists()

    def set_list_title(self, list_index, list_title):
        self.data[list_index]['title'] = list_title
        self.save_lists()
        self.refresh_lists()

    def save_lists(self):
        with open(self.lists_fn, 'w') as fd:
            json.dump(self.data, fd)

    def load_lists(self):
        if not exists(self.lists_fn):
            return
        with open(self.lists_fn) as fd:
            data = json.load(fd)
        self.data = data

    def refresh_lists(self):
        data = self.data
        self.data = []
        self.data = data

    def go_lists(self):
        # self.transition.direction = 'right'
        self.parent.current = 'lists'

    @property
    def lists_fn(self):
        return join(self.user_data_dir, 'lists.json')
    def listBtn(self, TextInput):
        # self.listItem = ObjectProperty(None)
        self.listItem = ListItemWithCounter()
        self.ids.listGrid.add_widget(self.listItem)
        self.list.text = ''
        # self.listItem.id = str(self.list.text)
        self.listItem.bind(on_release= self.rmv)

    def rmv(self, *args, **kwargs):
        print('yay')
        self.parent.current='ListWindow'
        self.parent.transition.direction = "left"


class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''



class MainWindow(Screen):

    #     self.load_lists()
    #
    # def load_lists(self):
    #     if not exists(self.lists_fn):
    #         return
    #     with open(self.lists_fn) as fd:
    #         lists = json.load(fd)
    #contains the bottom navigation and all the windows
    pass


class RecipesWindow(Screen):
    pass



class CalendarWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

# kv = Builder.load_file("groceriesApp.kv")

class saveApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"

        # Window.size = (400, 800)
        # mw = MainWindow()
        # return my_screenmanager
        return MainWindow()



if __name__ =="__main__":
    saveApp().run()
