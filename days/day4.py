from kivy.uix.label import Label
import numpy as np
from utils import data_manager as dm


def count_xmas_occurence(data):
    def search(row, word):
        count = 0
        for i in range(len(row) - len(word) + 1):
            if row[i:i + len(word)] == word:
                count += 1
        return count

    count = 0
    for row in data:
        count += search(row, "XMAS")
        count += search(row, "SAMX")

    x = len(data[0])
    y = len(data)

    for i in range(x):
        column = "".join([row[i] for row in data])
        count += search(column, "XMAS")
        count += search(column, "SAMX")

    a = np.array([list(row) for row in data]).reshape(x,y)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    for diag in diags:
        count += search("".join(diag), "XMAS")
        count += search("".join(diag), "SAMX")
    return count

def count_x_mas_occurence(data):
    count = 0
    x = len(data[0])
    y = len(data)
    for i in range(x-2):
        for j in range(y-2):
            if(data[j+1][i+1]=="A"):
                if(data[j][i] == "M" and data[j+2][i+2] == "S" and data[j+2][i] == "M" and data[j][i+2] == "S"):
                    count += 1
                elif (data[j][i] == "S" and data[j + 2][i + 2] == "M" and data[j + 2][i] == "M" and data[j][i+2] == "S"):
                    count += 1
                elif (data[j][i] == "M" and data[j + 2][i + 2] == "S" and data[j + 2][i] == "S" and data[j][i+2] == "M"):
                    count += 1
                elif (data[j][i] == "S" and data[j + 2][i + 2] == "M" and data[j + 2][i] == "S" and data[j][i+2] == "M"):
                    count += 1
    return count


def handle_day(layout, sample=False):
    data = dm.read_data(4, sample, False)
    answer = ""

    # * Part one
    answer += "Part one: "+str(count_xmas_occurence(data))

    # * Part two
    answer += "\nPart two: " + str(count_x_mas_occurence(data))

    dm.write_data(4, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




