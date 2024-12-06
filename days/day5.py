from kivy.uix.label import Label

from utils import data_manager as dm

def check_is_valid(page_update, instructions):
    for i in range(len(page_update)):
        for j in range(i,len(page_update)):
            # if([page_update[i], page_update[j]] in instructions):
            #     continue
            if([page_update[j], page_update[i]] in instructions):
                return False
    return True


def fix_page(page_update, instructions):
    for i in range(len(page_update)):
        for j in range(i,len(page_update)):
            if([page_update[j], page_update[i]] in instructions):
                page_update[i], page_update[j] = page_update[j], page_update[i]
                fix_page(page_update, instructions)
                return page_update
    return page_update


def handle_day(layout, sample=False):
    data = dm.split_array_at_empty(dm.read_data(5, sample, False))
    answer = ""
    instructions = [row.split('|') for row in data[0]]
    page_numbers = [row.split(',') for row in data[1]]

    # * Part one and two
    tmp_answer1 = 0
    tmp_answer2 = 0
    for page_update in page_numbers:
        if(check_is_valid(page_update, instructions)):
            tmp_answer1 += int(page_update[len(page_update)//2])
        else:
            fixed_page_update = fix_page(page_update, instructions)
            tmp_answer2 += int(fixed_page_update[len(fixed_page_update)//2])


    answer += "Part one: "+str(tmp_answer1)
    answer += "\nPart two: "+str(tmp_answer2)

    dm.write_data(5, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




