from routine import save_routine, print_routine
import random
import datetime

def ask_for_feedback(routine):
    """Collect feedback for each task in the routine and modify the routine accordingly."""
    print("\nPlease provide feedback for each task.")
    feedback = []

    # Collect feedback for each task in the routine
    for entry in routine:
        if entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            while True:
                try:
                    rating = int(input(f"Rate the placement of '{entry['task']}' (1-5): ").strip())
                    if rating < 1 or rating > 5:
                        raise ValueError("Rating must be between 1 and 5.")
                    feedback.append({"task": entry["task"], "rating": rating, "time": entry["time"]})
                    break  # Exit loop if input is valid
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a number between 1 and 5.")

    # Create a new routine with adjusted task placements
    improved_routine = []
    for entry in routine:
        # Keep high-rated tasks (4 or 5) in place
        if entry["task"] in [f["task"] for f in feedback if f["rating"] >= 4]:
            improved_routine.append(entry)
        elif entry["task"] not in ["Lunch Break", "10-Minute Break", "Free Time"]:
            # Find a new time slot for low-rated tasks
            new_time_slot = find_new_time_slot(improved_routine, entry["time"])
            improved_routine.append({"time": new_time_slot, "task": entry["task"]})
        else:
            # Retain all breaks and "Free Time" slots
            improved_routine.append(entry)

    # Save and print the improved routine for user review
    save_routine(improved_routine)
    print("\nAdjusted Routine:")
    print_routine(improved_routine)


def find_new_time_slot(improved_routine, original_time):
    """
    Find a new time slot for a task, ensuring it doesn't overlap with any existing entries
    and is as far as possible from the original time slot.
    """
    # Extract time ranges from current improved routine
    occupied_times = [entry["time"] for entry in improved_routine]

    # Generate potential time slots for a drastic change (far from original_time)
    all_possible_times = generate_possible_time_slots()

    # Filter out occupied times and select one far from original placement
    available_times = [t for t in all_possible_times if t not in occupied_times and t != original_time]

    # Randomly select an available time slot to add variability to the placement
    if available_times:
        return random.choice(available_times)
    else:
        # If no alternative is available, return the original time slot as fallback
        return original_time


def generate_possible_time_slots():
    """
    Generate a list of potential time slots for the day.
    Here, we create times at 1-hour intervals starting from 06:00 to 20:00.
    """
    time_slots = []
    current_time = datetime.time(6, 0)
    while current_time < datetime.time(20, 0):
        next_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(hours=1)).time()
        time_slots.append(f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}")
        current_time = next_time
    return time_slots
