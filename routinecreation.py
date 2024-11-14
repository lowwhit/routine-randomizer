import datetime
import json
import os
import random

from utilities import add_minutes, merge_free_time_slots, print_routine

# Basic time constants
START_TIME = datetime.time(6, 0)
LUNCH_START = datetime.time(12, 30)
LUNCH_END = datetime.time(13, 30)
END_TIME = datetime.time(20, 0)

# Routine creation functions

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
                schedule.append({"time": f"{LUNCH_START.strftime('%H:%M')} - {LUNCH_END.strftime('%H:%M')}", "task": "Lunch Break"})
                current_time = LUNCH_END
                continue

            work_time = min(task_time, 60)
            end_time = add_minutes(current_time.strftime("%H:%M"), work_time)
            schedule.append({"time": f"{current_time.strftime('%H:%M')} - {end_time}", "task": task["name"]})
            current_time = datetime.datetime.strptime(end_time, "%H:%M").time()
            task_time -= work_time

            if task_time > 0:
                break_end_time = add_minutes(current_time.strftime("%H:%M"), 10)
                schedule.append({"time": f"{current_time.strftime('%H:%M')} - {break_end_time}", "task": "10-Minute Break"})
                current_time = datetime.datetime.strptime(break_end_time, "%H:%M").time()

    while current_time < END_TIME:
        if LUNCH_START <= current_time < LUNCH_END:
            schedule.append({"time": f"{LUNCH_START.strftime('%H:%M')} - {LUNCH_END.strftime('%H:%M')}", "task": "Lunch Break"})
            current_time = LUNCH_END
        else:
            end_time = add_minutes(current_time.strftime("%H:%M"), 60)
            schedule.append({"time": f"{current_time.strftime('%H:%M')} - {end_time}", "task": "Free Time"})
            current_time = datetime.datetime.strptime(end_time, "%H:%M").time()

    return merge_free_time_slots(schedule)

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