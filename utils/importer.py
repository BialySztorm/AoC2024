import importlib
import os


def import_days():
    days = []
    files = [
        file for file in os.listdir('days')
        if file.endswith('.py') and file != '__init__.py'
    ]

    # Sort files numerically based on the number in the filename
    files.sort(key=lambda file: int(file[3:-3]))

    for file in files:
        module = importlib.import_module(f'days.{file[:-3]}')
        days.append(module)

    print(days)
    return days
