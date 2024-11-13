from routine import create_routine, load_routine, print_routine, save_routine
from feedback import ask_for_feedback

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
