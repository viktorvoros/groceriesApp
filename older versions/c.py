from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from string import ascii_letters

# this kv code defines two things:
# - the root widget, a vertical boxlayout with:
#   - the first element being another boxlayout to store buttons, with a
#   "button" id
#   - the second element being the ScreenManager that will contain our
#   screens, with "sm" id
# - a dynamic class rule, that defines the `MahButton` class, based on
#   button, and whose only difference with button is that on_press, it
#   changes the screen manager's screen to the one with the name equals
#   to the button's text.
#   This works by using using the app's root widget, and its `ids`
#   member, that maps the ids defined in the root widget's rule (ids
#   being local to rules), to get the ScreenManager object and change
#   its current screen. self is the current widget, here any `MahButton`
#   instance that is currently being pressed, so self.text is the text
#   displayed by the clicked button.


kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 30
        id: buttons
    ScreenManager:
        id: sm
<MahButton>:
    on_press: app.root.ids.sm.current = self.text
'''


class MahButton(Button):
    pass


class MahApp(App):
    '''
    Our main application
    '''
    def build(self):
        # here we load the kv code, so we get the root rule as root, and
        # the MahButton dynamic class is defined
        self.root = Builder.load_string(kv)

        for l in ascii_letters:
            # create a screen with a Label as content, and add it to the
            # ScreenManager object, again using ids, since the rule has
            # been loaded.
            s = Screen(name=l)
            s.add_widget(Label(text=l))
            self.root.ids.sm.add_widget(s)

            # add a button with the same text as the screen name to the
            # `buttons` id of root, using the same ids technique
            self.root.ids.buttons.add_widget(MahButton(text=l))

        # we need to return the root widget
        return self.root

# common python idiom to make programs that behave well if imported as
# modules
if __name__ == '__main__':
    MahApp().run()
