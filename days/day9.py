from kivy.uix.label import Label

from utils import data_manager as dm


class Block:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __repr__(self):
        return f"[{self.id}, {self.size}]"


def handle_day(layout, sample=False):
    data = dm.read_data(9, sample, False)[0]
    answer = ""

    # * Part one
    id = 0
    is_space = False
    blocks = []

    for block in list(data):
        if (is_space):
            for i in range(int(block)):
                blocks.append('.')
            is_space = False
        else:
            for i in range(int(block)):
                blocks.append(str(id))
            is_space = True
            id += 1
    # print(blocks)

    p1_blocks = blocks.copy()

    i = 0
    while i < len(p1_blocks):
        if (p1_blocks[i] == '.'):
            p1_blocks[i] = p1_blocks[len(p1_blocks) - 1]
            p1_blocks.pop()
            # print(p1_blocks)
            i -= 1
        i += 1

    sum = 0
    for i, block in enumerate(p1_blocks):
        sum += int(block) * i

    answer += f"Part one: {sum}\n"

    # * Part two
    p2_blocks = blocks.copy()
    blocks = []
    currernt_id = '0'
    counter = 0
    for block in p2_blocks:
        if (block == currernt_id):
            counter += 1
        else:
            if (currernt_id == '.'):
                blocks.append(Block(None, counter))
            else:
                blocks.append(Block(currernt_id, counter))
            currernt_id = block
            counter = 1
    blocks.append(Block(currernt_id, counter))
    # print(blocks)

    i = len(blocks) - 1
    while i > 0:
        if (blocks[i].id == None):
            i -= 1
            continue
        for j in range(i):
            if (blocks[j].id == None and blocks[j].size >= blocks[i].size):
                block = blocks.pop(i)
                left = blocks[j].size - block.size
                blocks.insert(i, Block(None, block.size))
                blocks.pop(j)
                blocks.insert(j, block)
                if (left > 0):
                    blocks.insert(j + 1, Block(None, left))
                    i += 1
                break
        i -= 1
    # print(blocks)

    sum = 0
    i = 0
    for block in blocks:
        for j in range(block.size):
            if (block.id != None):
                sum += int(block.id) * i
            i += 1

    answer += f"Part two: {sum}"

    dm.write_data(9, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
