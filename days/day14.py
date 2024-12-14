from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from PIL import Image
from io import BytesIO
from utils import data_manager as dm


def ganarate_image(map, index, save=True):
    height = len(map)
    width = len(map[0])
    image = Image.new('RGB', (width, height), 'white')
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            if map[y][x] > 0:
                pixels[x, y] = (0, 0, 0)  # Black for cells with value 1 or more
    if save:
        image.save(f'data/output/day14/{index}.bmp')
    else:
        multiplier = 5
        new_size = (width * multiplier, height * multiplier)
        image = image.resize(new_size)
        image_bytes = BytesIO()
        image.save(image_bytes, format="BMP")
        image_bytes.seek(0)
        return image_bytes


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
        # save_map_as_image(map, i + 1)

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

def has_5x5_block(map):
    height = len(map)
    width = len(map[0])
    for y in range(height - 4):
        for x in range(width - 4):
            if all(map[y + dy][x + dx] > 0 for dy in range(5) for dx in range(5)):
                return True
    return False


def print_maps(data):
    for i in range(100, 10000):
        data, map = simulate_motion(data, 101, 103)
        # save_map_as_image(map, i + 1)
        if has_5x5_block(map):
            print(f"5x5 block found at iteration {i + 1}")
            return i + 1, map



def handle_day(layout, sample=False):
    data = dm.read_data(14, sample)
    data = [[int(value) for value in row[0].split("=")[1].split(",") + row[1].split("=")[1].split(",")] for row in data]
    answer = ""

    # * Part one
    answer += f"Part one: {get_safety_factor(data, sample)}"

    dm.write_data(14, answer, sample)
    if not sample:
        i,map = print_maps(data)
        answer += f"\nPart two: {i}"
        image_bytes = ganarate_image(map, i,False)
        core_image = CoreImage(image_bytes, ext='bmp')
        layout.add_widget(KivyImage(texture=core_image.texture, size_hint=(1, 1)))


    # * Visualization
    y = 0.45
    if not sample:
        y = 0.9
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": y}))

