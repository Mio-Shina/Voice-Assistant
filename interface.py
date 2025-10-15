# Experimental one

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color
from kivymd.app import MDApp

class MyApp(MDApp):
    def build(self):
        root = FloatLayout()

        background = Image(source='c:/Users/Nijat/Downloads/gradient_1000_800.png', allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        self.title_label = Label(
            text="Голосовой помощник",
            font_size='40sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            text_size=(None, None)
        )
        self.subtitle_label = Label(
            text="Краткое описание ассистента",
            font_size='18sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(None, None),
            text_size=(None, None)
        )

        root.add_widget(self.title_label)
        root.add_widget(self.subtitle_label)

        self.update_text_size(root)

        img = Image(source='c:/Users/Nijat/Downloads/gradient_1000_800 (2).png').texture
        size = 100

        with root.canvas:
            Color(1, 1, 1, 1)
            self.ellipse = Ellipse(texture=img, size=(size, size))

        root.bind(size=self.update_size)

        return root

    def update_text_size(self, root):
        window_width = root.width
        window_height = root.height
        
        title_font_size = max(20, window_width / 20)
        subtitle_font_size = max(14, window_width / 30)
        
        self.title_label.font_size = title_font_size
        self.subtitle_label.font_size = subtitle_font_size

        self.title_label.size = self.title_label.texture_size
        self.subtitle_label.size = self.subtitle_label.texture_size

        self.title_label.pos = (root.width / 2 - self.title_label.width / 2, root.height * 0.9 - self.title_label.height / 2)
        self.subtitle_label.pos = (root.width / 2 - self.subtitle_label.width / 2, root.height * 0.75 - self.subtitle_label.height / 2)

    def update_size(self, instance, value):
        self.update_text_size(instance)

        x = instance.width / 2 - self.ellipse.size[0] / 2
        y = instance.height / 4 - self.ellipse.size[1] / 2
        self.ellipse.pos = (x, y)

if __name__ == '__main__':
    MyApp().run()
