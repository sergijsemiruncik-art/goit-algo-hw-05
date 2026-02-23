'''
Завдання 1
'''
def caching_fibonacci():
    #Creating an empty dictionary for caching
    cache = {}
    #Inner function for calculating Fibonacci sequence
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    return fibonacci

caching_fibonacci()
'''
Завдання 2
'''
import re

def generator_numbers(text: str):
    '''
    Iterates over the string `text`, finds all numbers
    and returns them one by one as `float`.
    '''
    for numbers in re.findall(r'\s[-+]?\d*\.\d+|\d+\s ', text):
        yield float(numbers)

def sum_profit(text: str, func: callable):
    '''
    Calculates the sum of profit from `text`
    '''
    total_income = 0
    for numbers in func(text):
        total_income += numbers
    return total_income

text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)

print(total_income)

'''
Завдання 3 у bot.py
'''

'''
Завдання 4
'''
import sys
from collections import Counter
from datetime import datetime

# Supported log levels (used for validation, counting, and display order).
allowed_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}

def parse_log_line(line: str) -> dict | None:
    """
      Parse one log line into a structured dictionary.

      Expected format:
      YYYY-MM-DD HH:MM:SS LEVEL message text...

      Returns:
          dict with keys: date, time, level, message
          None if the line is invalid.
      """
    cleaned_line = line.strip()

    if cleaned_line == "":
        return None

    parts = cleaned_line.split(maxsplit=3)
    if len(parts) != 4:
        return None

    date, time, level, message = parts
    level = level.upper()

    # Validate level name
    if level not in allowed_levels:
        return None

    # Validate date/time format
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }

def load_logs(file_path: str) -> list:
    """
       Load and parse logs from a file.
    """
    try:
        with open(file_path, 'r', encoding= 'UTF-8') as file:

            return [parsed for line in file if (parsed := parse_log_line(line)) is not None]

    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission denied")
    except IsADirectoryError:
        print("Path is a directory, not a file")
    except UnicodeDecodeError:
        print("File is not valid UTF-8")
    except OSError as error:
        print(f"OS error: {error}")
    return []

def filter_logs_by_level(logs: list, level: str) -> list:
    """
        Filter parsed logs by a given level.
    """

    target = level.upper()
    return list(filter(lambda log: log.get("level") == target, logs))

def count_logs_by_level(logs: list) -> dict:
    """
       Count logs per level.
    """
    try:
        levels = list(map(lambda log: log["level"], logs))
        counter = Counter(levels)
        return {lvl: counter.get(lvl, 0) for lvl in allowed_levels}
    except KeyError:
        print("Key not found")

def display_log_counts(counts: dict):
    """
       Print log counts as a simple table in a stable level order.
    """
    header = f'{"Logging level"} | {"Quantity"}'
    print(header)
    print('-' * len(header))
    for level in allowed_levels:
        count = counts.get(level, 0)
        print(f'{level} | {count}')

def main():

    if len(sys.argv) not in (2, 3):
        print("ERROR")
        return
    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if len(logs) == 0:
        print("No logs found")

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered = filter_logs_by_level(logs, level)

        print("")
        print(f"Details for {level.upper()}:")

        if len(filtered) == 0:
            print("No logs found")
        else:
            for log in filtered:
                print(log)

if __name__ == "__main__":
    main()