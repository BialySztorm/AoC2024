from platform import processor

from kivy.uix.label import Label

from math import log, floor
from utils import data_manager as dm


class BlinkProcessor:
    def __init__(self):
        self.tracking = {}

    def blink(self, stone, times):
        if times == 0:
            return 1

        if (stone, times) in self.tracking:
            return self.tracking[(stone, times)]

        if stone == 0:
            size = self.blink(1, times - 1)
        else:
            digits = floor(log(stone, 10)) + 1
            if digits % 2 == 0:
                left = stone // 10 ** (digits // 2)
                right = stone % 10 ** (digits // 2)
                size = self.blink(left, times - 1) + self.blink(right, times - 1)
            else:
                size = self.blink(stone * 2024, times - 1)

        self.tracking[(stone, times)] = size
        return size


def handle_day(layout, sample=False):
    data = dm.read_data(11, sample)[0]
    answer = ""

    # * Part one and two
    processor = BlinkProcessor()
    result = sum([processor.blink(int(stone), 25) for stone in data])

    answer += f"Part one: {result}\n"

    result = sum([processor.blink(int(stone), 75) for stone in data])

    answer += f"Part two: {result}"

    dm.write_data(11, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
