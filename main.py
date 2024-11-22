import random

from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '450')

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Quad


# noinspection PyUnresolvedReferences,PyArgumentList
class MainWidget(Widget):
    from transforms import (transform_2d, transform_perspective, transform)
    from user_actions import (on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up, keyboard_closed)
    perspective_x = NumericProperty(0)
    perspective_y = NumericProperty(0)

    v_num_lines = 10
    v_line_spacing = .25
    vertical_lines = []

    h_num_lines = 15
    h_line_spacing = .1
    horizontal_lines = []

    speed = 3
    current_offset_y = 0

    speed_x = 12
    current_speed_x = 0
    current_offset_x = 0

    num_tiles = 20
    tiles = []
    tiles_coordinates = []

    current_y_loop = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f"init; w:{self.width} , h:{self.height}")
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.generate_tiles_coordinates()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    @staticmethod
    def is_desktop():
        if platform in ('linux', 'win', 'macos'):
            return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.num_tiles):
                self.tiles.append(Quad())

    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.num_tiles):
            r = random.randint(0, 2)
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            last_y += 1

    def update_tiles(self):
        for i in range(0, self.num_tiles):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            x_min, y_min = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            x1, y1 = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.v_num_lines):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)

            for i in range(self.h_num_lines):
                self.horizontal_lines.append(Line())

    def update_vertical_lines(self):
        start_index = -int(self.v_num_lines / 2) + 1
        for i in range(start_index, start_index + self.v_num_lines):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = -int(self.v_num_lines / 2) + 1
        end_index = start_index + self.v_num_lines - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)

        for i in range(self.h_num_lines):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_x
        spacing = self.v_line_spacing * self.width
        offset = index - 0.5

        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.h_line_spacing * self.height

        line_y = index * spacing_y - self.current_offset_y

        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.speed * time_factor

        spacing_y = self.h_line_spacing * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1
            self.generate_tiles_coordinates()

        self.current_offset_x += self.current_speed_x * time_factor


class GalaxyApp(App):
    pass


GalaxyApp().run()
