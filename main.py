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

    return merge_free_time_slots(schedule)

def merge_free_time_slots(schedule):
    """Merges continuous 'Free Time' slots into one if they exceed 2 hours."""
    merged_schedule = []
    free_start = None
    free_end = None

    for entry in schedule:
        if entry["task"] == "Free Time":
            if not free_start:
                free_start = entry["time"].split(" - ")[0]
            free_end = entry["time"].split(" - ")[1]
        else:
            if free_start and free_end:
                start_dt = datetime.datetime.strptime(free_start, "%H:%M")
                end_dt = datetime.datetime.strptime(free_end, "%H:%M")
                duration = (end_dt - start_dt).total_seconds() / 3600

                if duration > 2:
                    merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
                else:
                    merged_schedule.extend([{"time": f"{free_start} - {free_end}", "task": "Free Time"}])
                free_start, free_end = None, None

            merged_schedule.append(entry)

    if free_start and free_end:
        start_dt = datetime.datetime.strptime(free_start, "%H:%M")
        end_dt = datetime.datetime.strptime(free_end, "%H:%M")
        duration = (end_dt - start_dt).total_seconds() / 3600
        if duration > 2:
            merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
        else:
            merged_schedule.extend([{"time": f"{free_start} - {free_end}", "task": "Free Time"}])

    return merged_schedule

def print_routine(routine):
    """Prints the routine in a MySQL-style table format with serial numbers and merged free time slots."""
    print("\nYour Daily Routine:")
    print("+-----+---------------------+----------------------+")
    print("| No. |       Time         |        Task          |")
    print("+-----+---------------------+----------------------+")

    for i, entry in enumerate(routine, start=1):
        print(f"| {i:<3} | {entry['time']:<19} | {entry['task']:<20} |")
        print("+-----+---------------------+----------------------+")

def save_routine(routine, iteration):
    """Save each iteration of the routine to the file."""
    with open("routine.txt", "a") as file:
        file.write(f"\nIteration {iteration}:\n")
        for entry in routine:
            file.write(f"{entry['time']} - {entry['task']}\n")
        file.write("\n" + "=" * 40 + "\n")
    print(f"Iteration {iteration} saved to 'routine.txt'.")

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

    save_routine(improved_routine, "Feedback Adjusted")

def main():
    print("Routine Randomizer")
    mode = int(input("Choose mode:\n1 - Create a new routine\n2 - Load existing routine\nEnter choice: "))

    if mode == 1:
        routine = create_routine()
        print_routine(routine)
        iteration = 1 if not os.path.exists("routine.txt") else sum(1 for line in open("routine.txt") if line.startswith("Iteration")) + 1
        save_routine(routine, iteration)
        ask_for_feedback(routine)
    elif mode == 2:
        load_routine()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
