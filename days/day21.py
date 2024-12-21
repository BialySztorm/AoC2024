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

# ! Keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

def write_text(text,keypad,start):
    y = start[1]
    x = start[0]
    seq = ""
    empty_pos = [0,0]
    for i in range(len(keypad)):
        if None in keypad[i]:
            empty_pos = [keypad[i].index(None),i]
            break
    for char in text:
        char_pos = [0,0]
        for i in range(len(keypad)):
            if char in keypad[i]:
                char_pos = [keypad[i].index(char),i]
                break
        if y == empty_pos[1]:
            y_vector = char_pos[1] - y
            x_vector = char_pos[0] - x
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
            y_vector = char_pos[1] - y
            x_vector = char_pos[0] - x
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
    numeric_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"],[None, "0", "A"]]
    directional_keypad = [[None,"^","A"], ["<","v",">"]]

    sum = 0
    for row in data:
        robot1_seq = write_text(row, numeric_keypad,[2,3])
        robot2_seq = write_text(robot1_seq, directional_keypad,[2,0])
        my_seq = write_text(robot2_seq, directional_keypad,[2,0])
        control_sum = int(row[0]+row[1]+row[2])
        sum += control_sum * len(my_seq)

    answer += f"Part one: {sum}\n"

    # * Part one and two


    dm.write_data(21, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




