import datetime
import json
import os
import random

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

def print_routine(routine):
    print("\nYour Daily Routine:")
    print("+-----+---------------------+----------------------+")
    print("| No. |       Time         |        Task          |")
    print("+-----+---------------------+----------------------+")

    for i, entry in enumerate(routine, start=1):
        print(f"| {i:<3} | {entry['time']:<19} | {entry['task']:<20} |")
        print("+-----+---------------------+----------------------+")