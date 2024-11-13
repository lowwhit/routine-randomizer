import datetime
import json
import os

# Basic time constants
START_TIME = datetime.time(6, 0)
LUNCH_START = datetime.time(12, 30)
LUNCH_END = datetime.time(13, 30)
END_TIME = datetime.time(20, 0)

def add_minutes(time, minutes):
    """Helper function to add minutes to a time object."""
    dt = datetime.datetime.combine(datetime.date.today(), time)
    dt += datetime.timedelta(minutes=minutes)
    return dt.time()

def create_routine():
    tasks = []
    num_tasks = int(input("How many tasks do you have? "))

    for i in range(num_tasks):
        task_name = input(f"Enter the name of task {i + 1}: ")
        task_duration = int(input(f"How long (in minutes) does '{task_name}' take? "))
        task_priority = int(input(f"What is the priority of '{task_name}' (1 = high, 3 = low)? "))
        tasks.append({"name": task_name, "duration": task_duration, "priority": task_priority})

    # Sort tasks based on priority (1 is the highest priority)
    tasks = sorted(tasks, key=lambda t: t["priority"])
    schedule = []
    current_time = START_TIME

    for task in tasks:
        task_time = task["duration"]
        while task_time > 0:
            if current_time >= END_TIME:
                break  # End the day if the time reaches the end time

            if LUNCH_START <= current_time < LUNCH_END:
                schedule.append({"time": f"{LUNCH_START.strftime('%H:%M')} - {LUNCH_END.strftime('%H:%M')}", "task": "Lunch Break"})
                current_time = LUNCH_END
                continue

            work_time = min(task_time, 60)  # Work for 60 minutes before a break
            end_time = add_minutes(current_time, work_time)
            schedule.append({"time": f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}", "task": task["name"]})
            current_time = end_time
            task_time -= work_time

            if task_time > 0:
                # Add a 10-minute break
                break_end_time = add_minutes(current_time, 10)
                schedule.append({"time": f"{current_time.strftime('%H:%M')} - {break_end_time.strftime('%H:%M')}", "task": "10-Minute Break"})
                current_time = break_end_time

    while current_time < END_TIME:
        if LUNCH_START <= current_time < LUNCH_END:
            schedule.append({"time": f"{LUNCH_START.strftime('%H:%M')} - {LUNCH_END.strftime('%H:%M')}", "task": "Lunch Break"})
            current_time = LUNCH_END
        else:
            end_time = add_minutes(current_time, 60)
            schedule.append({"time": f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}", "task": "Free Time"})
            current_time = end_time

    return schedule

def print_routine(routine):
    print("\nYour Daily Routine:")
    print(f"{'Time':<20} {'Task':<20}")
    print("-" * 40)
    for entry in routine:
        print(f"{entry['time']:<20} {entry['task']:<20}")

def save_routine(routine):
    with open("routine.txt", "w") as file:
        json.dump(routine, file)
    print("Routine saved to 'routine.txt'.")

def load_routine():
    if os.path.exists("routine.txt"):
        with open("routine.txt", "r") as file:
            routine = json.load(file)
            print_routine(routine)
            ask_for_feedback(routine)
    else:
        print("No routine file found. Create a new routine first.")

def ask_for_feedback(routine):
    print("\nPlease provide feedback for each task.")
    feedback = []

    for entry in routine:
        if entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            rating = int(input(f"Rate the placement of '{entry['task']}' (1-5): "))
            feedback.append({"task": entry["task"], "rating": rating})

    improved_routine = []
    for entry in routine:
        if entry["task"] in [f["task"] for f in feedback if f["rating"] >= 4]:
            improved_routine.append(entry)
        elif entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            improved_routine.append({"time": entry["time"], "task": "Free Time"})
        else:
            improved_routine.append(entry)

    save_routine(improved_routine)

def main():
    print("Routine Randomizer")
    mode = int(input("Choose mode:\n1 - Create a new routine\n2 - Load existing routine\nEnter choice: "))

    if mode == 1:
        routine = create_routine()
        print_routine(routine)
        save_routine(routine)
        ask_for_feedback(routine)
    elif mode == 2:
        load_routine()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
