from src.classes import Abonnent
import time


def main():
    while True:
        number = input("Enter your phone number (or press RETURN to exit): ")
        if not number:
            break
        abonnent = Abonnent(int(number))
        time.sleep(1)
        if abonnent.enter_status:
            while True:
                print("\nSelect an action:\n1 - Call statistics\n2 - Call history with other contact\n3 - Exit")
                choice = int(input("Your choice (enter a number): "))
                if choice == 1:
                    abonnent.statistics()
                elif choice == 2:
                    target_user = int(input("Enter the target phone number: "))
                    while not target_user:
                        target_user = int(input("Phone number not found. Try again: "))
                    abonnent.history(target_user)
                else:
                    break
                time.sleep(1)

    print("<exiting program>")
    time.sleep(1)


if __name__ == '__main__':
    main()
