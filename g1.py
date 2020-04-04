import json
from os.path import join, exists
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import ILeftBodyTouch,IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, AliasProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.picker import MDDatePicker
import matplotlib
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
# mpl_use('module://kivy.garden.matplotlib.backend_kivy')
# style.use('dark_background')


class ScreenManagementHome(ScreenManager):
    transition = 'left'
    def go_lists(self):
        self.transition.direction = 'right'
        self.current = 'lists'
    # list_number = StringProperty()
    pass

class ChartWindow(Screen, BoxLayout):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    def __init__(self, **kwargs):
        super(ChartWindow, self).__init__(**kwargs)
        self.fig, self.ax1 = plt.subplots()
        self.ax1.pie([5,1,2], radius=1)
        self.mpl_canvas = self.fig.canvas
        self.add_widget(self.mpl_canvas)
    pass

class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_screen = NumericProperty()
    list_number = StringProperty()
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()
    # print(list_number)

class SwipeButton(Carousel):
    list_title = StringProperty()
    list_content = StringProperty()
    list_index = NumericProperty()
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(SwipeButton, self).__init__(**kwargs)
        print (self.caller)

class ListItem(TwoLineAvatarIconListItem):
    '''Custom list item.'''
    list_title = StringProperty()
    list_content = StringProperty()
    list_index = NumericProperty()

    icon = StringProperty("android")


class ItemPopup(Popup):
    list_title = StringProperty()
    list_content = StringProperty()
    list_index = NumericProperty()
    def __init__(self, **kwargs):
        self.caller = kwargs.pop('caller')
        super(ItemPopup, self).__init__(**kwargs)

    def on_open(self):
        self.background = 'transp.png'
        # print (self.caller)

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

class HomeWindow(Screen,MDApp):

    data = ListProperty()
    # list_number = StringProperty()

    def _get_data_for_widgets(self):
        return [{
            'list_index': index,
            'list_content': item['content'],
            'list_title': item['title'],
            'list_number': item['number'],
            'list_screen': item['screen']
            }
            for index, item in enumerate(self.data)]

    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

    def __init__(self,**kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.load_lists()
        self.nb = 0

    def clearTxt(self, TextInput):
        self.list.text = ''

    def add_list(self, textinput, number, screen):
        self.data.append({'title': textinput, 'content': '', 'number': number, 'screen': screen})
        list_index = len(self.data) - 1
        num = [0]
        for i in range(0,len(self.data)):
            num.append((int(self.data[i]['screen'])))
        next_screen = str(max(num) + 1)
        self.data[list_index]['screen'] = next_screen
        self.refresh_lists()
        self.save_lists()
        self.nb += 1
        # self.list.text = ''
        # self.edit_list(list_index)
        # print(self.nb)

    def edit_list(self, list_index, list_number, list_screen):
        list = self.data[list_index]
        # print(list)
        name = 'list{}'.format(list_screen)

        if self.parent.has_screen(name):
            self.parent.remove_widget(self.parent.get_screen(name))

        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        self.parent.add_widget(view)
        self.parent.transition.direction = 'left'
        numberOfItems = str(int(view.list_number) + 1)
        self.list_number = numberOfItems
        self.data[list_index]['number'] = str(view.list_number)
        self.parent.current = view.name
        # self.refresh_lists()

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
        # print(self.data)

    def refresh_data(self, list_index, list_number):
        data = self.data[list_index]
        data['number'] = list_number
        self.data[list_index] = []
        self.data[list_index] = data
        self.save_lists()
        # print(self.data)

    # def go_lists(self):
    #     self.parent.transition.direction = 'right'
    #     self.parent.current = 'lists'

    def del_list(self, list_index, list_screen):
        list = self.data[list_index]
        name = 'list{}'.format(list_screen)
        view = ListWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        # print(view.data)
        view.empty_list()
        del self.data[list_index]
        # self.save_lists()
        self.refresh_lists()
        self.parent.go_lists()
        # print(self.data)

    @property
    def lists_fn(self):
        return join(self.user_data_dir, 'lists.json')

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
        self.item_number = 0


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
        print(self.data)
        self.save_items()

    def item_info(self, list_index, list_title):
        popup = ItemPopup(caller = self, title='', list_title=list_title, size_hint=(None, None), size=(self.size[0]-20, 350))
        popup.open()
        self.item_number = list_index
    def edit_item(self, list_title):
        list = self.data[self.item_number]
        print(self.list_number)

        self.list_number = str(len(self.data))
        # popup = ItemPopup(caller = self,title=list_title, size_hint=(None, None), size=(400, 400))
        # print(list_index)
        self.data[self.item_number]['title'] = list_title

        # popup.open()
        self.refresh_items()
        self.save_items()
        # if self.parent.has_screen(name):
        #     self.parent.remove_widget(self.sm.get_screen(name))
        #
        # view = ChartWindow(name=name, list_index=list_index, list_title=list.get('title'), list_content=list.get('content'))
        # self.parent.add_widget(view)
        # # self.transition.direction = 'left'
        # self.parent.current = view.name

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

    def empty_list(self):
        self.data = []
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
        print(self.data)

    # def refresh_item_data(self, list_index, list_number):
    #     data = self.data[list_index]
    #     data['number'] = list_number
    #     self.data[list_index] = []
    #     self.data[list_index] = data
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


class CalendarWindow(Screen, BoxLayout):
    def __init__(self,**kwargs):
        super(CalendarWindow,self).__init__(**kwargs)
        self.add_widget(MDDatePicker(callback=self.get_date))
        # time_dialog.open()

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''

class SettingsWindow(Screen):
    pass

# kv = Builder.load_file("groceriesApp.kv")
class g1App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        Window.size = (400, 800)
        return MainWindow()


if __name__ =="__main__":
    g1App().run()
