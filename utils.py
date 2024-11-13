import datetime

def add_minutes(time, minutes):
    """Helper function to add minutes to a time object."""
    dt = datetime.datetime.combine(datetime.date.today(), datetime.time(time[0], time[1]))
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
                    merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
                free_start, free_end = None, None

            merged_schedule.append(entry)

    if free_start and free_end:
        start_dt = datetime.datetime.strptime(free_start, "%H:%M")
        end_dt = datetime.datetime.strptime(free_end, "%H:%M")
        duration = (end_dt - start_dt).total_seconds() / 3600
        if duration > 2:
            merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})
        else:
            merged_schedule.append({"time": f"{free_start} - {free_end}", "task": "Free Time"})

    return merged_schedule
