import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty, AliasProperty
from os.path import join, exists
import json

class RecipesWindow(Screen):
    data = ListProperty()

    def _get_data_for_recipes(self):
        return[{'r_index': index,
                'r_category': item['category'],
                'r_title': item['title'],
                'r_content': item['content'],
                'r_photo': item['photo'],
                'r_author': item['author'],
                'r_time': item['time'],
                'r_date': item['date'],
                'r_books': item['books']}
                for index, item in enumerate(self.data)]

    data_for_recipes = AliasProperty(_get_data_for_recipes, bind=['data'])

    def __init__(self,**kwargs):
        super(RecipesWindow, self).__init__(**kwargs)
        self.load_data()
        self.add_item()

    def load_data(self):
        if not exists('data/recipes.json'):
            return
        with open('data/recipes.json') as fd:
            data = json.load(fd)
        self.data = data

    def save_data(self):
        with open('data/recipes.json'.format(self.name), 'w') as fd:
            json.dump(self.data, fd)

    def refresh_data(self):
        data = self.data
        self.data = []
        self.data = data
        self.save_data()

    def empty_data(self):
        self.data = []
        self.refresh_items()

    def add_item(self):
        self.data.append({'category': 'category', 'title': 'title',
                        'content': 'content', 'photo': 'photo',
                        'author': 'author', 'time': 'time',
                        'time': 'time', 'date': 'date', 'books': 'books'})
        self.refresh_data()


class RecipeItem(BoxLayout):
    r_index = NumericProperty()
    r_category = StringProperty()
    r_title = StringProperty()
    r_content = StringProperty()
    r_photo = StringProperty()
    r_author = StringProperty()
    r_time = StringProperty()
    r_date = StringProperty()
    r_books = StringProperty()
