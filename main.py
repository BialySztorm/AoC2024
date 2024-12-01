from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from utils.importer import import_days


class CalendarDay(Button):
    def __init__(self, day, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.text = str(day)
        self.color = (0.8, 0, 0, 1)
        self.disabled_color = (0.8, 0.8, 0.8, 1)
        self.background_color = (0.8, 0.3, 0.3, 1)  # Less visible by default
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.hovered = False

    def on_mouse_pos(self, *args):
        if (self.disabled):
            return
        pos = args[1]
        if self.collide_point(*self.to_widget(*pos)):
            if not self.hovered:
                self.hovered = True
                self.on_mouse_enter()
        else:
            if self.hovered:
                self.hovered = False
                self.on_mouse_leave()

    def on_mouse_enter(self):
        Window.set_system_cursor('hand')

    def on_mouse_leave(self):
        Window.set_system_cursor('arrow')


class MyApp(App):
    def build(self):
        Window.maximize()
        self.days = import_days()
        self.sample = False
        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Ustaw kolor tła (R, G, B, A)
            self.rect = Rectangle(size=Window.size)
        self.show_main()

        return self.layout

    def show_main(self, *args):
        self.layout.clear_widgets()
        self.calendar_layout = GridLayout(cols=7, rows=6, padding=200)

        for _ in range(6):
            self.calendar_layout.add_widget(Widget())

        for day in range(1, 32):
            day_layout = RelativeLayout()
            day_button = CalendarDay(day)
            day_button.disabled = True
            day_layout.add_widget(day_button)
            if day == 25:
                image = Image(source='assets/images/christmas.png', size_hint=(0.8, 0.8))
                image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
                day_layout.add_widget(image)
            self.calendar_layout.add_widget(day_layout)

        for j in range(len(self.days)):
            day_button = self.calendar_layout.children[30 - j].children[0]
            day_button.background_color = (0.8, 0.8, 0.8, 0.8)
            day_button.disabled = False

            day_button.bind(on_press=lambda x, i=j: self.show_day(i))

        self.layout.add_widget(self.calendar_layout)

        sample_btn = Button(text='Sample?', size_hint=(None, None), size=(200, 50), pos_hint={'x': 0, 'top': 1},
                            pos=(50, -50))
        sample_btn.bind(on_press=self.switch_sample)
        self.layout.add_widget(sample_btn)
        self.sample_text = Label(text=str(self.sample), size_hint=(None, None), size=(200, 50), pos_hint={'top': 1},
                                 pos=(200, -50))
        self.layout.add_widget(self.sample_text)

    def show_day(self, day, *args):
        self.layout.clear_widgets()

        return_btn = Button(text='Return to calendar', size_hint=(None, None), size=(200, 50),
                            pos_hint={'x': 0, 'top': 1}, pos=(50, -50))
        return_btn.bind(on_press=self.show_main)
        print("Day", day + 1)
        self.days[day].handle_day(self.layout, self.sample)
        self.layout.add_widget(return_btn)

    def switch_sample(self, *args):
        self.sample = not self.sample
        self.sample_text.text = str(self.sample)


if __name__ == '__main__':
    MyApp().run()
