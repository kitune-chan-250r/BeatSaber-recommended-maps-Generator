import ScoreSaber
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

list_sample = ["RIOT - Overkill Expert+", "Camellia - NUCLEAR-STAR Expert+", "Silent Siren - Routine Expert+"]

class MainScreen(Screen):
    """docstring for MainScreen"""
    grid_l = ObjectProperty(None)
    top_lbl = ObjectProperty(None)

    def button_plessed(self):
        for i in range(3):
                layout = GridLayout(cols=1)
                img = Image(source='kivy.png')
                lbl = Label(text='label')
                layout.add_widget(img)
                layout.add_widget(lbl)

                btn1 = Button(size_hint=(1, None))
                btn1.text = '%r' % i
                btn1.add_widget(layout)

                grid.add_widget(btn1)
    
class MainApp(App):

    """docstring for MainApp"""
    def build(self):
        app = MainScreen()
        return app


if __name__ == '__main__':
    MainApp().run()