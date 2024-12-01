import importlib
import os

def import_days():
    days = []
    for file in os.listdir('days'):
        if file.endswith('.py') and file != '__init__.py':
            module = importlib.import_module(f'days.{file[:-3]}')
            days.append(module)
    return days