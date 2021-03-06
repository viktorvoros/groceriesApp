import json
from kivy.storage.jsonstore import JsonStore
from os.path import join, exists
import kivy
from kivy.lang import Builder
from kivy.clock import Clock
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
from matplotlib.figure import Figure
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
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

class ScreenManagementChart(ScreenManager):
    pass

class ChartWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    stat = ListProperty()
    spent = 0.0
    # lab = ObjectProperty(None)
    # lab.text='2'

    def __init__(self, **kwargs):
        global canvas
        super(ChartWindow, self).__init__(**kwargs)

        self.plotStat()
        self.fig, self.ax1 = plt.subplots()

        plt.bar(1,self.spent)



        Clock.schedule_once(self._do_setup)

    def _do_setup(self, *l):
        self.pl()

    def pl(self):

        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.ids.box.add_widget(canvas)
        canvas.draw()

    def updatePlot(self):
        # self.plotStat()
        plt.clf()
        # plt.bar(1, self.spent)
        # canvas.draw()
        # fig, ax = plt.subplots()
        # plt.bar('Mar', self.spent)
        # self.canvas.draw

    def loadStat(self):
        if not exists('stat.json'.format(self.name)):
            return
        with open('stat.json'.format(self.name)) as fd:
            stat = json.load(fd)
        self.stat = stat

    # def changeLabel(self):
    #     self.ids.lab.text = 'pressed'
    #     self.ch.ids.gr.add_widget(Button(text='added'))

    def plotStat(self):
        self.loadStat()
        nam = []
        for i in range(0,len(self.stat)):
            nam.append(float(self.stat[i]['quantity'])* float(self.stat[i]['price']))
        print(sum(nam))
        self.spent =sum(nam)
        # fig, ax = plt.subplots()
        # plt.bar(1, self.spent)
        # canvas = fig.canvas
class MyFigure(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super(MyFigure, self).__init__(plt.gcf(), **kwargs)
        fig, ax = plt.subplots()
        plt.bar(1, 2)
        canvas = fig.canvas
        self.add_widget(canvas)


class ListItemWithCounter(OneLineAvatarIconListItem):
    '''List of shopping list'''
    list_screen = NumericProperty()
    list_number = StringProperty()
    list_content = StringProperty()
    list_title = StringProperty()
    list_index = NumericProperty()
    # print(list_number)

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
    # print(item_category)
    icon = StringProperty("food")

class CategoryIcon(MDIconButton, IRightBodyTouch):
    item_category = StringProperty()
    def __init__(self, **kwargs):
        super(CategoryIcon, self).__init__(**kwargs)
        # self.item_category = SwipeButton().item_category
        if self.item_category == 'Dairy':
            icon = StringProperty("food")
        else:
            icon = StringProperty("android")

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
        # print (self.caller)

class CounterLabel(IRightBodyTouch, MDLabel):
    # pass
    list_number = NumericProperty()
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
        with open('h.json', 'w') as fd:
            json.dump(self.data, fd)

    def load_lists(self):
        if not exists('h.json'):
            return
        with open('h.json') as fd:
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


    # @property
    # def lists_fn(self):
    #     return join(self.user_data_dir + 'mydir\\', 'lists.json')
    # @property
    # def items_fn(self):
    #     return join(self.user_data_dir, 'items.json')

class ListWindow(Screen):
    list_index = NumericProperty()
    list_title = StringProperty()
    list_content = StringProperty()
    list_number = StringProperty()
    list_screen = StringProperty()
    data = ListProperty()
    item_database = ListProperty()
    statistics_database = ListProperty()
    allTogether = []
    spent = 3.0


    def _get_data_for_items(self):
        return [{
            'list_index': index,
            'item_name': item['name'],
            'item_category': item['category'],
            'item_price': item['price'],
            'item_note': item['note'],
            'item_image': item['image'],
            'item_quantity': item['quantity']}
            for index, item in enumerate(self.data)]

    data_for_items = AliasProperty(_get_data_for_items, bind=['data'])

    def _get_data_for_item_database(self):
        return [{'item_index': index,
                'item_name': item['name'],
                'item_category': item['category'],
                'item_price': item['price'],
                'item_note': item['note'],
                'item_image': item['image'],
                }
                for index, item in enumerate(self.item_database)]

    data_for_items_database = AliasProperty(_get_data_for_item_database, bind=['item_database'])

    def add_item_to_database(self, name, category, quantity, price, note, image):
        nam = []
        for i in range(0, len(self.item_database)):
            nam.append(self.item_database[i]['name'])

        if name not in nam:
            self.item_database.append({'name': name, 'category': category, 'price': price, 'note': note, 'image': image})
            self.save_item_database()
        else:
            pass
        # print('add: ', self.item_database)
        # self.refresh_item_database(name, category,price,image)
    def refresh_item_database(self, name, category, price, image):
        nam = []
        for i in range(0, len(self.item_database)):
            if name == self.item_database[i]['name']:
                if self.item_database[i]['category'] != category:
                    self.item_database[i]['category'] = category
                if self.item_database[i]['price'] != price:
                    self.item_database[i]['price'] = price
                if self.item_database[i]['image'] != image:
                    self.item_database[i]['image'] = image

        database = self.item_database
        self.item_database = []
        self.item_database = database
        self.save_item_database()
        print('refresh: ', self.item_database)

    def save_item_database(self):
        with open('item_database.json', 'w') as fd:
            json.dump(self.item_database, fd)

    def load_item_database(self):
        if not exists('item_database.json'):
            return
        with open('item_database.json') as fd:
            item_database = json.load(fd)
        self.item_database = item_database
        # print('load: ', self.item_database)

    def __init__(self,**kwargs):
        super(ListWindow, self).__init__(**kwargs)
        self.root = ScreenManagementHome()
        self.home = HomeWindow()
        self.ch = ChartWindow()
        self.load_item_database()
        self.load_items()
        self.loadStatistics()
        self.list_number = str(len(self.data))
        self.item_number = 0
        print(self.name)


    def add_item(self, textinput):
        database = self.item_database
        item_category = ''
        item_price = '0'
        item_image = ''
        for i in range(0,len(database)):
            if textinput == database[i]['name']:
                item_category = database[i]['category']
            if textinput == database[i]['name']:
                item_price = database[i]['price']
            if textinput == database[i]['name']:
                item_image = database[i]['image']

        self.data.append({'name': textinput, 'category': item_category, 'price': item_price, 'note': '', 'image': item_image, 'quantity':'1'})
        list_index = len(self.data) - 1
        self.list_number = str(len(self.data))
        self.save_items()
        self.save_item_database()

    def item_info(self, item_index, item_name):
        self.load_items()
        item_category = self.data[item_index]['category']
        item_quantity = self.data[item_index]['quantity']
        item_price = self.data[item_index]['price']
        item_note = self.data[item_index]['note']
        item_image = self.data[item_index]['image']
        popup = ItemPopup(caller = self, title='', item_name=item_name, item_category=item_category, item_price=item_price, item_quantity=item_quantity,item_note=item_note, item_image=item_image, size_hint=(None, None), size=(self.size[0]-20, 350))
        popup.open()
        self.item_number = item_index

    def edit_item(self, item_name, item_category, item_quantity, item_price, item_note, item_image):
        list = self.data[self.item_number]
        self.list_number = str(len(self.data))
        self.data[self.item_number]['name'] = item_name
        self.data[self.item_number]['category'] = item_category
        self.data[self.item_number]['quantity'] = item_quantity
        self.data[self.item_number]['price'] = item_price
        self.data[self.item_number]['note'] = item_note
        self.data[self.item_number]['image'] = item_image
        self.refresh_items()
        self.save_items()
        self.refresh_item_database(item_name, item_category, item_price, item_image)
        self.save_item_database()

    def load_items(self):
        # print(self.list_index)
        if not exists('{}.json'.format(self.name)):
            return
        with open('{}.json'.format(self.name)) as fd:
            data = json.load(fd)
        self.data = data
        self.list_number = str(len(self.data))

    def clearTxt(self, TextInput):
        self.item.text = ''

    def del_item(self, list_index):
        del self.data[list_index]
        self.refresh_items()
        self.save_items()


    def empty_list(self):
        self.data = []
        self.save_items()
        self.refresh_items()

    def save_items(self):
        with open('{}.json'.format(self.name), 'w') as fd:
            json.dump(self.data, fd)

    def refresh_items(self):
        data = self.data
        self.data = []
        self.data = data
        self.list_number = str(len(self.data))
        print(self.data)

    def tobespent(self, data):
        add = []
        for i in range(0, len(self.data)):
            add.append(float(self.data[i]['quantity'])* float(self.data[i]['price']))
        return str(sum(add))

    def add_to_statistics(self, index, data):
        self.statistics_database.append(data[index])
        self.allTogether.append(float(data[index]['quantity'])* float(data[index]['price']))
        spentSum = sum(self.allTogether)
        self.spent = spentSum
        self.saveStatistics()

    def loadStatistics(self):
        if not exists('stat.json'.format(self.name)):
            return
        with open('stat.json'.format(self.name)) as fd:
            stat = json.load(fd)
        self.statistics_database = stat

    def saveStatistics(self):
        with open('stat.json', 'w') as fd:
            json.dump(self.statistics_database, fd)
    # def items_fn(self):
    #     return join(self.user_data_dir, 'items.json')
    # @property
    # def item_database_fn(self):
    #     return join(self.user_data_dir, 'item_database.json')

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

        return MainWindow()


if __name__ =="__main__":
    g1App().run()
