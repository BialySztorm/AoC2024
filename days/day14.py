from kivy.uix.label import Label
from PIL import Image
from utils import data_manager as dm


def save_map_as_image(map, index):
    height = len(map)
    width = len(map[0])
    image = Image.new('RGB', (width, height), 'white')
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            if map[y][x] > 0:
                pixels[x, y] = (0, 0, 0)  # Black for cells with value 1 or more

    image.save(f'data/output/day14/{index}.bmp')


def simulate_motion(data, width, height):
    map = [[0 for _ in range(width)] for _ in range(height)]
    for i, row in enumerate(data):
        x = (row[0] + row[2]) % width
        y = (row[1] + row[3]) % height
        data[i] = [x, y, row[2], row[3]]
        map[y][x] = map[y][x] + 1

    return data, map


def get_safety_factor(data, sample):
    if (sample):
        width = 11
        height = 7
    else:
        width = 101
        height = 103
    map = []
    for i in range(100):
        data, map = simulate_motion(data, width, height)
        save_map_as_image(map, i + 1)

    count1, count2, count3, count4 = 0, 0, 0, 0
    for y in range(height):
        for x in range(width):
            if x < width // 2 and y < height // 2:
                count1 += map[y][x]
            elif x > width // 2 and y < height // 2:
                count2 += map[y][x]
            elif x < width // 2 and y > height // 2:
                count3 += map[y][x]
            elif x > width // 2 and y > height // 2:
                count4 += map[y][x]

    for row in map:
        print(row)

    return count1 * count2 * count3 * count4

def print_maps(data):
    for i in range(100,10000):
        data, map = simulate_motion(data, 101, 103)
        save_map_as_image(map, i+1)


def handle_day(layout, sample=False):
    data = dm.read_data(14, sample)
    data = [[int(value) for value in row[0].split("=")[1].split(",") + row[1].split("=")[1].split(",")] for row in data]
    answer = ""

    # * Part one
    answer += f"Part one: {get_safety_factor(data, sample)}"

    dm.write_data(14, answer, sample)

    print_maps(data)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
