from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty 
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.uix.image import Image
"""
class SongnameView(RecycleView):
    def __init__(self, **kwargs):
        super(SongnameView, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(5)]
"""
class SongImageView(RecycleView):
    def __init__(self, **kwargs):
        super(SongImageView, self).__init__(**kwargs)
        self.data = [{"source": "kivy.png"} for x in range(5)]




class Test(App):
    def build(self):
        #root = Builder.load_string(KV)
        #root.data = [item for item in items]
        return RecycleView()


Test().run()