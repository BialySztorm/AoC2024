def read_data(day, sample=False):
    if(sample):
        with open(f"data/input/sample_day{day}.txt") as f:
            return f.read().strip().split("\n")
    with open(f"data/input/day{day}.txt") as f:
        return f.read().strip().split("\n")

def write_data(day, data, sample=False):
    print(data)
    if(sample):
        with open(f"data/output/sample_day{day}.txt", "w") as f:
            f.write(data)
        return
    with open(f"data/output/day{day}.txt", "w") as f:
        f.write(data)