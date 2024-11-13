# 🗓️ Routine Randomizer

A simple Python program that helps you create a balanced daily routine based on your tasks and priorities. The Routine Randomizer schedules tasks with breaks and lunch, while also allowing you to provide feedback to improve the routine over time using a local search approach.

## 🚀 Features
- **Task Scheduling**: Automatically schedules tasks based on priority and duration.
- **Break Management**: Adds a 10-minute break after every 60 minutes of work.
- **Lunch Break**: Fixed lunch break from 12:30 PM to 1:30 PM.
- **Daily Timeframe**: Day starts at 6:00 AM and ends at 8:00 PM.
- **Feedback-Based Improvement**: Allows you to rate each task's placement and improves future routines based on your feedback.
- **Save and Load**: Save your routine to a file for later use, or load an existing routine to review and refine.

## 📝 How It Works
1. **Create a New Routine**: Enter your tasks, time estimates, and priorities.
2. **Automatic Scheduling**: The program organizes tasks into a daily routine, inserting breaks and free time where appropriate.
3. **Feedback Loop**: After trying the routine, rate each task's placement (1-5). Tasks rated highly are retained in future routines, while low-rated ones are replaced with "Free Time."
4. **Save & Load**: Save your daily routine to `routine.txt` for future reference, and load it up anytime to review or update based on your feedback.

## 🛠️ Setup and Usage

### Prerequisites
- **Python 3.x**: Make sure Python is installed on your system.

### Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/routine-randomizer.git
   cd routine-randomizer


