import json
from os.path import join, exists
import kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, AliasProperty
from ListWindow import *
from ScreenManagementHome import *

class HomeWindow(Screen):

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
        
        # self.load_item_database()
        print(self.data)
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
        self.refresh_lists()

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
        with open('data/h.json', 'w') as fd:
            json.dump(self.data, fd)

    def load_lists(self):
        if not exists('data/h.json'):
            return
        with open('data/h.json') as fd:
            data = json.load(fd)
        self.data = data

    def refresh_lists(self):
        data = self.data
        self.data = []
        self.data = data
        self.save_lists()
        # print(self.data)

    def refresh_data(self, list_index, list_number):
        data = self.data[list_index]
        data['number'] = list_number
        self.data[list_index] = []
        self.data[list_index] = data
        self.save_lists()
        # self.refresh_lists()
        print(self.data)

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
