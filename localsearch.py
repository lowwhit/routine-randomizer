import datetime
import json
import os
import random

from routinecreation import save_routine
from utilities import print_routine

# Feedback and local search functions

def ask_for_feedback(routine):
    print("\nPlease provide feedback for each task.")
    feedback = []

    for entry in routine:
        if entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            while True:
                try:
                    rating = int(input(f"Rate the placement of '{entry['task']}' (1-5): ").strip())
                    if rating < 1 or rating > 5:
                        raise ValueError("Rating must be between 1 and 5.")
                    feedback.append({"task": entry["task"], "rating": rating, "time": entry["time"]})
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a number between 1 and 5.")

    improved_routine = []
    for entry in routine:
        if entry["task"] in [f["task"] for f in feedback if f["rating"] >= 4]:
            improved_routine.append(entry)
        elif entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            new_time_slot = find_new_time_slot(improved_routine, entry["time"])
            improved_routine.append({"time": new_time_slot, "task": entry["task"]})
        else:
            improved_routine.append(entry)

    save_routine(improved_routine)
    print("\nAdjusted Routine:")
    print_routine(improved_routine)

def find_new_time_slot(improved_routine, original_time):
    occupied_times = [entry["time"] for entry in improved_routine]
    all_possible_times = generate_possible_time_slots()
    available_times = [t for t in all_possible_times if t not in occupied_times and t != original_time]

    if available_times:
        return random.choice(available_times)
    else:
        return original_time

def generate_possible_time_slots():
    time_slots = []
    current_time = datetime.time(6, 0)
    while current_time < datetime.time(20, 0):
        next_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(hours=1)).time()
        time_slots.append(f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}")
        current_time = next_time
    return time_slots