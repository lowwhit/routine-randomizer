import json
import os
from utils import add_minutes, merge_free_time_slots

START_TIME = (6, 0)
LUNCH_START = (12, 30)
LUNCH_END = (13, 30)
END_TIME = (20, 0)

def create_routine():
    tasks = []
    num_tasks = int(input("How many tasks do you have? "))

    for i in range(num_tasks):
        task_name = input(f"Enter the name of task {i + 1}: ")
        task_duration = int(input(f"How long (in minutes) does '{task_name}' take? "))
        task_priority = int(input(f"What is the priority of '{task_name}' (1 = high, 3 = low)? "))
        tasks.append({"name": task_name, "duration": task_duration, "priority": task_priority})

    tasks = sorted(tasks, key=lambda t: t["priority"])
    schedule = []
    current_time = START_TIME

    for task in tasks:
        task_time = task["duration"]
        while task_time > 0:
            if current_time >= END_TIME:
                break
            if LUNCH_START <= current_time < LUNCH_END:
                schedule.append({"time": f"{LUNCH_START} - {LUNCH_END}", "task": "Lunch Break"})
                current_time = LUNCH_END
                continue

            work_time = min(task_time, 60)
            end_time = add_minutes(current_time, work_time)
            schedule.append({"time": f"{current_time} - {end_time}", "task": task["name"]})
            current_time = end_time
            task_time -= work_time

            if task_time > 0:
                break_end_time = add_minutes(current_time, 10)
                schedule.append({"time": f"{current_time} - {break_end_time}", "task": "10-Minute Break"})
                current_time = break_end_time

    while current_time < END_TIME:
        if LUNCH_START <= current_time < LUNCH_END:
            schedule.append({"time": f"{LUNCH_START} - {LUNCH_END}", "task": "Lunch Break"})
            current_time = LUNCH_END
        else:
            end_time = add_minutes(current_time, 60)
            schedule.append({"time": f"{current_time} - {end_time}", "task": "Free Time"})
            current_time = end_time

    return merge_free_time_slots(schedule)

def print_routine(routine):
    print("\nYour Daily Routine:")
    print("+-----+---------------------+----------------------+")
    print("| No. |       Time         |        Task          |")
    print("+-----+---------------------+----------------------+")

    for i, entry in enumerate(routine, start=1):
        print(f"| {i:<3} | {entry['time']:<19} | {entry['task']:<20} |")
        print("+-----+---------------------+----------------------+")

def save_routine(routine):
    routines = []
    if os.path.exists("routine.txt"):
        with open("routine.txt", "r") as file:
            try:
                routines = json.load(file)
            except json.JSONDecodeError:
                pass

    routines.append(routine)

    with open("routine.txt", "w") as file:
        json.dump(routines, file, indent=4)
    print("Routine saved to 'routine.txt'.")

def load_routine():
    if os.path.exists("routine.txt"):
        with open("routine.txt", "r") as file:
            routines = json.load(file)
            print_routine(routines[-1])
            return routines[-1]
    else:
        print("No routine file found. Create a new routine first.")
        return None
