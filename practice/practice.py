from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.metrics import dp

from kivy.properties import StringProperty, BooleanProperty, Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget


# Widgets example
class WidgetEx(GridLayout):
    num = 0
    my_text = StringProperty(str(num))
    txt_validate = StringProperty(str(""))
    is_toggled = BooleanProperty(False)

    # slider_value_txt = StringProperty(str(50))

    def on_button_click(self):
        print("clicked")
        if self.is_toggled:
            self.num += 1
            self.my_text = str(self.num)

    def on_toggle_button_state(self, widget):
        print(f"toggled: {widget.state}")
        if widget.state == "normal":
            widget.text = "OFF"
            self.is_toggled = False
        else:
            widget.text = "ON"
            self.is_toggled = True

    @staticmethod
    def on_switch_active(widget):
        print(f"Switch: {str(widget.active)}")

    @staticmethod
    def on_slider_value(widget):
        # self.slider_value_txt = str(int(widget.value))
        print(f"Slider: {str(int(widget.value))}")

    def on_text_validate(self, widget):
        self.txt_validate = widget.text


# Stack layout example
class StackLayoutEx(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.orientation = "rl-tb"

        size = dp(100)

        for i in range(100):
            b = Button(text=str(i + 1), size_hint=(None, None), size=(size, size))
            self.add_widget(b)


# Can be replaced in the .kv file directly (/currentmain.kv).
# class GridLayoutEx(GridLayout):
#   pass


class AnchorLayoutEx(AnchorLayout):
    pass


# in code example of adding widget and buttons.
class BoxLayoutEx(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        b1 = Button(text="A")
        b2 = Button(text="B")
        b3 = Button(text="C")

        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)


class MainWidget(Widget):
    pass


class CanvasEx1(Widget):
    pass


class CanvasEx2(Widget):
    pass


class CanvasEx3(Widget):
    pass


class CanvasEx4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100, 100, 400, 500), width=3)
            Color(1, 0, 0)
            Line(circle=(400, 200, 80), width=2)
            Line(rectangle=(600, 200, 200, 100), width=2)

            Color(0, 1, 0)
            self.rect = Rectangle(pos=(600, 400), size=(200, 100))

    def on_button_click(self):
        x, y = self.rect.pos
        w, h = self.rect.size
        inc = dp(10)

        diff = self.width - (x + w + 3)

        if diff < inc:
            inc = diff

        x += inc
        self.rect.pos = (x, y)


# 427,827
class CanvasEx5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ball_size = dp(100)
        self.velo_x = dp(3)
        self.velo_y = dp(3)

        with self.canvas:
            self.ball = Ellipse(pos=(300, 300), size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update, 1 / 120)

    def on_size(self, *args):
        # print(f"On size: {str(self.width)},{self.height}")
        self.ball.pos = (
            self.center_x - self.ball_size / 2,
            self.center_y - self.ball_size / 2,
        )

    def update(self, dt):
        # print("update")
        x, y = self.ball.pos

        x += self.velo_x
        y += self.velo_y

        if y + self.ball_size > self.height:
            y = self.height - self.ball_size
            self.velo_y = -self.velo_y

        if x + self.ball_size > self.width:
            x = self.width - self.ball_size
            self.velo_x = -self.velo_x

        if y < 0:
            y = 0
            self.velo_y = -self.velo_y
        if x < 0:
            x = 0
            self.velo_x = -self.velo_x

        self.ball.pos = (x, y)


class CanvasEx6(Widget):
    pass


class CanvasEx7(BoxLayout):
    pass


class PracticeApp(App):
    pass


PracticeApp().run()
