from kivy.clock import Clock
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import data_manager as dm


def handle_day(layout, sample=False):
    data = dm.read_data(1, sample)
    answer = ""

    left = []
    right = []
    for item in data:
        l, r = item.split()
        left.append(l)
        right.append(r)
    left.sort()
    right.sort()

    # * Part one
    differences = [abs(int(left[i]) - int(right[i])) for i in range(len(data))]
    sum_part_one = sum(differences)
    answer = "Part one:\n" + str(sum_part_one) + "\n"

    # * Part two
    similarities = []
    for l in left:
        tmp = 0
        for r in right:
            if l == r:
                tmp += 1
        similarities.append(tmp * int(l))

    sum_part_two = sum(similarities)
    answer += "Part two:\n" + str(sum_part_two) + "\n"

    dm.write_data(1, answer, sample)

    # * Visualization
    fig, ax1 = plt.subplots()
    ax1.set_xlim(0, len(differences))
    ax1.set_ylim(0, max(differences) + 10)
    line1, = ax1.plot([], [], lw=2, label='Differences', color='blue')

    ax2 = ax1.twinx()
    ax2.set_ylim(0, max(similarities) + 10)
    line2, = ax2.plot([], [], lw=2, label='Similarities', color='red')

    # Add text to display cumulative sums
    sum_text1 = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, color='blue')
    sum_text2 = ax2.text(0.02, 0.90, '', transform=ax2.transAxes, color='red')

    def update_plot(dt):
        frame = update_plot.frame
        if frame >= len(differences):
            return  # Stop animating when all frames are done
        x = list(range(frame + 1))
        y1 = differences[:frame + 1]
        y2 = similarities[:frame + 1]
        line1.set_data(x, y1)
        line2.set_data(x, y2)
        sum_text1.set_text(f'Cumulative Sum (Differences): {sum(y1)}')
        sum_text2.set_text(f'Cumulative Sum (Similarities): {sum(y2)}')
        fig.canvas.draw()  # Update canvas
        update_plot.frame += 1

    update_plot.frame = 0

    Clock.schedule_interval(update_plot, 1 / 240)  # 240 FPS

    # Add the plot to the Kivy layout
    plot_widget = FigureCanvasKivyAgg(fig, pos_hint={"center_x": 0.5, "center_y": 0.5})
    layout.add_widget(plot_widget)
