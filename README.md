
# 📅 Daily Routine Scheduler

Welcome to the **Daily Routine Scheduler**! This Python project enables you to manage and automate your daily schedule, allowing flexibility in handling different tasks like exercise, study, and leisure time. 📈🕒

## 🌟 Features

- 📑 **Routine Creation**: Generate routines and save them in a JSON format.
- ⏰ **Task Timing**: Set specific tasks with allocated time intervals.
- 🔍 **Local Search**: Easily search through saved routines to find specific tasks or schedules.
- 🛠 **Utilities**: Additional utility functions for managing routines.

## 📂 File Structure

- `main.py` - Main entry point of the project.
- `localsearch.py` - Module for implementing local search and get feedback on the created routine
- `routinecreation.py` - Handles the creation and formatting of routines.
- `utilities.py` - Utility functions used across the project.
- `routine.txt` - JSON file containing sample routines.

## 🚀 Getting Started

### Prerequisites

- **Python 3.9**: Ensure you have Python installed on your machine.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/lowwhit/dailyroutine-randomizer.git
   cd routine-randomizer
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Run main script**: Execute `main.py` to start and test the complete functionality.

   ```bash
   python main.py
   ```

## 📜 Sample Routine Format

Each routine is stored in JSON format. Here’s an example:

```json
[
    {
        "time": "06:00 - 07:00",
        "task": "Algorithms"
    },
    {
        "time": "07:00 - 07:10",
        "task": "10-Minute Break"
    },
    {
        "time": "09:20 - 09:35",
        "task": "Meditate"
    }
]
```

## 🤖 Contributing

Contributions are welcome! Feel free to submit a PR or report any issues. 

1. **Fork the repository**.
2. **Create your feature branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`).
4. **Push to the branch** (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙋‍♂️ Support

If you encounter any issues or have questions, please feel free to reach out!

---

### 🔖 Note:
Ensure `routine.txt` and `utilities.py` are in the same directory to enable full functionality.
