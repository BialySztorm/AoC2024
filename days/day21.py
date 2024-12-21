from kivy.uix.label import Label

from utils import data_manager as dm

# ! Keypad
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# 638A - 70
# 965A - 66
# 780A - 66
# 803A - 76
# 246A - 70

# ! Keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+


def write_text(text):
    keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"],[None, "0", "A"]]
    y = 3
    x = 2
    seq = [""]
    empty_pos = [0,3]
    for char in text:
        char_pos = [0,0]
        for i in range(len(keypad)):
            if char in keypad[i]:
                char_pos = [keypad[i].index(char),i]
                break
        y_vector = char_pos[1] - y
        x_vector = char_pos[0] - x
        if y_vector != 0 and x_vector != 0:
            tmp1_seq = ""
            if y_vector > 0:
                tmp1_seq += "v"*y_vector
            else:
                tmp1_seq += "^"*abs(y_vector)
            if x_vector > 0:
                tmp1_seq += ">"*x_vector
            else:
                tmp1_seq += "<"*abs(x_vector)
            tmp2_seq = tmp1_seq[::-1]+"A"
            tmp1_seq += "A"
            tmp_seq = []
            for i in range(len(seq)):
                if not (y+y_vector == empty_pos[1] and x == empty_pos[0]):
                    tmp_seq.append(seq[i]+tmp1_seq)
                if not (x+x_vector == empty_pos[0] and y == empty_pos[1]):
                    tmp_seq.append(seq[i]+tmp2_seq)
            seq = tmp_seq

        else:
            tmp_seq = ""
            if y_vector > 0:
                tmp_seq += "v"*y_vector
            else:
                tmp_seq += "^"*abs(y_vector)
            if x_vector > 0:
                tmp_seq += ">"*x_vector
            else:
                tmp_seq += "<"*abs(x_vector)
            tmp_seq += "A"
            for i in range(len(seq)):
                seq[i] += tmp_seq

        x = char_pos[0]
        y = char_pos[1]
    return seq

def write_text2(text):
    keypad = [[None,"^","A"], ["<","v",">"]]
    y = 0
    x = 2
    empty_pos = [0,0]
    seq = ""
    for char in text:
        char_pos = [0,0]
        for i in range(len(keypad)):
            if char in keypad[i]:
                char_pos = [keypad[i].index(char),i]
                break
        y_vector = char_pos[1] - y
        x_vector = char_pos[0] - x
        if y == empty_pos[1]:
            if y_vector > 0:
                seq += "v"*y_vector
            else:
                seq += "^"*abs(y_vector)
            if x_vector > 0:
                seq += ">"*x_vector
            else:
                seq += "<"*abs(x_vector)
            seq += "A"
        else:
            if x_vector > 0:
                seq += ">"*x_vector
            else:
                seq += "<"*abs(x_vector)
            if y_vector > 0:
                seq += "v"*y_vector
            else:
                seq += "^"*abs(y_vector)
            seq += "A"
        x = char_pos[0]
        y = char_pos[1]
    return seq


def handle_day(layout, sample=False):
    data = [list(row) for row in dm.read_data(21, sample, False)]
    answer = ""

    # * Part one and two
    sum = 0
    for row in data:
        robot1_seq = write_text(row)
        print(robot1_seq)
        best = ''
        for seq in robot1_seq:
            robot2_seq = write_text2(seq)
            my_seq = write_text2(robot2_seq)
            if len(my_seq) < len(best) or best == '':
                best = my_seq
        control_sum = int(row[0]+row[1]+row[2])
        print(len(best))
        sum += control_sum * len(best)

    answer += f"Part one: {sum}\n"



    dm.write_data(21, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




