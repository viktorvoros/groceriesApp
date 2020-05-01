import json
from os.path import join, exists
import kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ListProperty, AliasProperty
from HomeWindow import *
from ScreenManagementHome import *
from ListItem import *

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

    def __init__(self,**kwargs):
        super(ListWindow, self).__init__(**kwargs)
        self.root = ScreenManagementHome()
        # self.home = HomeWindow()
        # self.ch = ChartWindow()
        self.load_item_database()
        self.load_items()
        self.loadStatistics()
        self.list_number = str(len(self.data))
        self.item_number = 0
        self.dairyLabel = 0.5
        self.meatLabel = 0.5
        print(self.name)

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
        with open('data/item_database.json', 'w') as fd:
            json.dump(self.item_database, fd)

    def load_item_database(self):
        if not exists('data/item_database.json'):
            return
        with open('data/item_database.json') as fd:
            item_database = json.load(fd)
        self.item_database = item_database
        # print('load: ', self.item_database)

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
        self.lineChart()

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
        if not exists('data/{}.json'.format(self.name)):
            return
        with open('data/{}.json'.format(self.name)) as fd:
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
        with open('data/{}.json'.format(self.name), 'w') as fd:
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
        return str(round(sum(add),2))

    def add_to_statistics(self, index, data):
        self.statistics_database.append(data[index])
        self.allTogether.append(float(data[index]['quantity'])* float(data[index]['price']))
        spentSum = sum(self.allTogether)
        self.spent = spentSum
        self.saveStatistics()

    def loadStatistics(self):
        if not exists('data/stat.json'.format(self.name)):
            return
        with open('data/stat.json'.format(self.name)) as fd:
            stat = json.load(fd)
        self.statistics_database = stat

    def saveStatistics(self):
        with open('data/stat.json', 'w') as fd:
            json.dump(self.statistics_database, fd)

    def lineChart(self):
        dairy = []
        meat = []
        for i in range(0, len(self.data)):
            cat = self.data[i]['category']
            if cat == 'Dairy':
                dairy.append(float(self.data[i]['price'])* float(self.data[i]['quantity']))
            if cat == 'Meat':
                meat.append(float(self.data[i]['price'])* float(self.data[i]['quantity']))

        spent = sum(dairy) + sum(meat)
        print(sum(meat), sum(dairy))
        self.ids.dairy.size_hint_x = str(sum(dairy)/spent)
        # self.ids.lineChart.add_widget(Label(text='added'))
        self.meat.size_hint_x= sum(meat)/spent
