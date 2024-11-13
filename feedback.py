from routine import save_routine

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
