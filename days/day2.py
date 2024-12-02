from utils import data_manager as dm
from enum import Enum

class ReportState(Enum):
    UNKNOWN= 0
    INCREASING = 2
    DECREASING = 3

class Reactor:
    def __init__(self, data):
        self.data = data

    def solve(self, use_dampener=False):
        self.dumpener = use_dampener
        safe_reports = 0
        for row in self.data:
            self.dumpener_used = False
            if self.check_levels(row):
                safe_reports += 1
            elif self.dumpener:
                dumped_rows = [row[:i] + row[i+1:] for i in range(len(row))]
                for dumped_row in dumped_rows:
                    if self.check_levels(dumped_row):
                        safe_reports += 1
                        self.dumpener_used = True
                        break

        return safe_reports

    def check_levels(self, row):
        tmp = int(row[0])
        is_safe = True
        state = ReportState.UNKNOWN
        for item in map(int, row[1:]):
            if (item > tmp and state != ReportState.DECREASING):
                if (state == ReportState.UNKNOWN):
                    state = ReportState.INCREASING
                if (item - tmp > 3):
                    is_safe = False
                    break
            elif (item < tmp and state != ReportState.INCREASING):
                if (state == ReportState.UNKNOWN):
                    state = ReportState.DECREASING
                if (tmp - item > 3):
                    is_safe = False
                    break
            else:
                is_safe = False
                break
            tmp = item
        return is_safe

def handle_day(layout, sample=False):
    data = dm.read_data(2, sample)
    answer = ""
    reactor = Reactor(data)

    # * Part one and two
    answer += "Part one:\n" + str(reactor.solve()) + "\n"
    answer += "Part two:\n" + str(reactor.solve(True)) + "\n"

    dm.write_data(2, answer, sample)
    # * Visualization

