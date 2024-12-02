def read_data(day, sample=False, split=True):
    if (sample):
        with open(f"data/input/sample_day{day}.txt") as f:
            data = f.read().strip().split("\n")
    else:
        with open(f"data/input/day{day}.txt") as f:
            data = f.read().strip().split("\n")
    if (split):
        return [item.split() for item in data]
    return data


def write_data(day, data, sample=False):
    print(data)
    if (sample):
        with open(f"data/output/sample_day{day}.txt", "w") as f:
            f.write(data)
        return
    with open(f"data/output/day{day}.txt", "w") as f:
        f.write(data)
