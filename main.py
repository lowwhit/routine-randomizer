import datetime
import json
import os
import random

# Basic time constants
START_TIME = datetime.time(6, 0)
LUNCH_START = datetime.time(12, 30)
LUNCH_END = datetime.time(13, 30)
END_TIME = datetime.time(20, 0)

# Utility functions

def add_minutes(time, minutes):
    """Helper function to add minutes to a time object."""
    if isinstance(time, str):
        time = datetime.datetime.strptime(time, "%H:%M").time()
        
    dt = datetime.datetime.combine(datetime.date.today(), time)
    dt += datetime.timedelta(minutes=minutes)
    return dt.time().strftime("%H:%M")

def merge_free_time_slots(schedule):
    """Merges continuous 'Free Time' slots into one if they exceed 2 hours."""
    merged_schedule = []
    free_start = None
    free_end = None

    for entry in schedule:
        if entry["task"] == "Free Time":
            if not free_start:
                free_start = entry["time"].split(" - ")[0].strip()
            free_end = entry["time"].split(" - ")[1].strip()
        else:
            if free_start and free_end:
                free_start = datetime.datetime.strptime(free_start, "%H:%M").strftime("%H:%M")
                free_end = datetime.datetime.strptime(free_end, "%H:%M").strftime("%H:%M")
                
                start_dt = datetime.datetime.strptime(free_start, "%H:%M")
                end_dt = datetime.datetime.strptime(free_end, "%H:%M")
                duration = (end_dt - start_dt).total_seconds() / 3600

                if duration > 2:
                    merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
                else:
                    merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
                free_start, free_end = None, None

            merged_schedule.append(entry)

    if free_start and free_end:
        free_start = datetime.datetime.strptime(free_start, "%H:%M").strftime("%H:%M")
        free_end = datetime.datetime.strptime(free_end, "%H:%M").strftime("%H:%M")
        
        start_dt = datetime.datetime.strptime(free_start, "%H:%M")
        end_dt = datetime.datetime.strptime(free_end, "%H:%M")
        duration = (end_dt - start_dt).total_seconds() / 3600
        if duration > 2:
            merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
        else:
            merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})

    return merged_schedule

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

def print_routine(routine):
    print("\nYour Daily Routine:")
    print("+-----+---------------------+----------------------+")
    print("| No. |       Time         |        Task          |")
    print("+-----+---------------------+----------------------+")

    for i, entry in enumerate(routine, start=1):
        print(f"| {i:<3} | {entry['time']:<19} | {entry['task']:<20} |")
        print("+-----+---------------------+----------------------+")

# Main function

def main():
    print("Routine Randomizer")
    mode = int(input("Choose mode:\n1 - Create a new routine\n2 - Load existing routine\nEnter choice: "))

    if mode == 1:
        routine = create_routine()
        print_routine(routine)
        save_routine(routine)
    elif mode == 2:
        routine = load_routine()
        if routine:
            feedback_choice = input("\nWould you like to provide feedback on this routine? (y/n): ").strip().lower()
            if feedback_choice == 'y':
                ask_for_feedback(routine)
            else:
                print("Exiting to main menu.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
