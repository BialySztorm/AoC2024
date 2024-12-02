from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from utils import data_manager as dm
from enum import Enum

class ReportState(Enum):
    UNKNOWN= 0
    INCREASING = 2
    DECREASING = 3

class Reactor:
    def __init__(self, data):
        self.data = data
        self.visual = []

    def solve(self, use_dampener=False):
        self.dumpener = use_dampener
        safe_reports = 0
        for row in self.data:
            self.dumpener_used = False
            if self.check_levels(row):
                safe_reports += 1
            elif self.dumpener:
                self.dumpener_used = True
                dumped_rows = [row[:i] + row[i+1:] for i in range(len(row))]
                for dumped_row in dumped_rows:
                    if self.check_levels(dumped_row):
                        safe_reports += 1
                        break

        return safe_reports

    def add_to_visual(self, row, wrong=-1):
        if(self.dumpener):
            self.visual.append([row, wrong, self.dumpener_used])

    def check_levels(self, row):
        tmp = int(row[0])
        is_safe = True
        state = ReportState.UNKNOWN
        for i, item in enumerate(map(int, row[1:]), start=1):
            if (item > tmp and state != ReportState.DECREASING):
                if (state == ReportState.UNKNOWN):
                    state = ReportState.INCREASING
                if (item - tmp > 3):
                    self.add_to_visual(row, i)
                    is_safe = False
                    break
            elif (item < tmp and state != ReportState.INCREASING):
                if (state == ReportState.UNKNOWN):
                    state = ReportState.DECREASING
                if (tmp - item > 3):
                    self.add_to_visual(row, i)
                    is_safe = False
                    break
            else:
                self.add_to_visual(row, i)
                is_safe = False
                break
            tmp = item
        if (is_safe):
            self.add_to_visual(row)
        return is_safe

    def get_visual(self):
        return self.visual


def handle_day(layout, sample=False):
    data = dm.read_data(2, sample)
    answer = ""
    reactor = Reactor(data)

    # * Part one and two
    answer += "Part one:\n" + str(reactor.solve()) + "\n"
    answer += "Part two:\n" + str(reactor.solve(True)) + "\n"

    dm.write_data(2, answer, sample)

    # * Visualization
    visual = reactor.get_visual()
    root = ScrollView(size_hint=(0.5, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
    container = BoxLayout(orientation='vertical', size_hint_y=None)
    container.bind(minimum_height=container.setter('height'))
    root.add_widget(container)
    layout.add_widget(root)

    bottom_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
    p1_label = Label(text="0", size_hint=(None, None), size=(50, 50))
    p2_label = Label(text="0", size_hint=(None, None), size=(50, 50))
    filler = BoxLayout(size_hint=(0.8, None), height=50)
    bottom_row.add_widget(filler)
    bottom_row.add_widget(p1_label)
    bottom_row.add_widget(p2_label)
    container.add_widget(bottom_row)

    def update_visual(dt, current_row=None, p1_correct=None, p2_correct=None):
        row_layout = BoxLayout( orientation="horizontal",size_hint=(1, None), height=50)
        row_container = BoxLayout(orientation='horizontal', size_hint=(0.8, None),height=50)
        row, error, dumped = visual[current_row]
        for i, item in enumerate(row):
            label = Label(text=item, size_hint=(None, None), size=(50, 50))
            if dumped:
                label.color = (1, 1, 0, 1)
            else:
                label.color = (0, 1, 0, 1)
            if i == error:
                label.color = (1, 0, 0, 1)
            row_container.add_widget(label)
        row_layout.add_widget(row_container)
        if error > 0:
            label1 = Label(text="X", size_hint=(None, None), size=(50, 50))
            label1.color = (1, 0, 0, 1)
            row_layout.add_widget(label1)
            label2 = Label(text="X", size_hint=(None, None), size=(50, 50))
            label2.color = (1, 0, 0, 1)
            row_layout.add_widget(label2)
        else:
            if dumped:
                label1 = Label(text="X", size_hint=(None, None), size=(50, 50))
                label1.color = (1, 0, 0, 1)
                row_layout.add_widget(label1)
                label2 = Label(text="✓", size_hint=(None, None), size=(50, 50))
                label2.color = (0, 1, 0, 1)
                row_layout.add_widget(label2)
                p2_correct += 1
            else:
                label1 = Label(text="✓", size_hint=(None, None), size=(50, 50))
                label1.color = (0, 1, 0, 1)
                row_layout.add_widget(label1)
                label2 = Label(text="✓", size_hint=(None, None), size=(50, 50))
                label2.color = (0, 1, 0, 1)
                row_layout.add_widget(label2)
                p1_correct += 1
                p2_correct += 1
        container.add_widget(row_layout, index=len(container.children) - 1)
        p1_label.text = str(p1_correct)
        p2_label.text = str(p2_correct)
        current_row += 1

        if len(container.children) > 50:
            container.remove_widget(container.children[0])

        if current_row < len(visual):
            Clock.schedule_once(lambda dt: update_visual(dt, current_row, p1_correct,p2_correct), 1/120)

    Clock.schedule_once(lambda dt: update_visual(dt, 0,0,0), 1/120)





