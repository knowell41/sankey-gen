import os
from src.cashflow import GenerateDataset

data = GenerateDataset()
heading = """
 _______  _______  _______           _______  _        _______                          _________ _______
(  ____ \(  ___  )(  ____ \|\     /|(  ____ \( \      (  ___  )|\     /|       |\     /|\__   __// ___   )
| (    \/| (   ) || (    \/| )   ( || (    \/| (      | (   ) || )   ( |       | )   ( |   ) (   \/   )  |
| |      | (___) || (_____ | (___) || (__    | |      | |   | || | _ | | _____ | |   | |   | |       /   )
| |      |  ___  |(_____  )|  ___  ||  __)   | |      | |   | || |( )| |(_____)( (   ) )   | |      /   /
| |      | (   ) |      ) || (   ) || (      | |      | |   | || || || |        \ \_/ /    | |     /   /
| (____/\| )   ( |/\____) || )   ( || )      | (____/\| (___) || () () |         \   /  ___) (___ /   (_/|
(_______/|/     \|\_______)|/     \||/       (_______/(_______)(_______)          \_/   \_______/(_______/

"""

print(heading)
print("Visualize your Cashflow!!")

mapping = {
    "1": "income",
    "2": "expenses",
    "3": "savings",
    "4": "bank",
    "5": "bank transaction",
}


def get_input():
    name = input(f"Name of this transaction: ")
    value = input(f"Value involved in this transaction: ")
    return name, value


def get_bank_transaction_detail():
    bank_name = input(f"Name of bank source: ")
    destination = input(f"Transaction name: ")
    amount = input(f"Amount: ")
    return bank_name, destination, amount


while True:
    raw_input = input(
        "Menu:\n"
        "[1] Add income\n"
        "[2] Add expenses\n"
        "[3] Add savings\n"
        "[4] Add banks\n"
        "[5] Add bank transaction\n"
        "[9] Work with existing output\n"
        "[0] Vizualize Cashflow\n\n"
        "Enter your choice: "
    )

    match raw_input:
        case "1":
            print("You selected: Add income")
            name, value = get_input()
            data.add_income(name, value)

            print("\n Income successfully added!\n")
        case "2":
            print("You selected: Add expenses")
            name, value = get_input()
            data.add_expenses(name, value)
        case "3":
            print("You selected: Add savings")
            name, value = get_input()
            data.add_savings(name, value)
        case "4":
            print("You selected: Add banks")
            name, value = get_input()
            data.add_bank(name, value)
        case "5":
            print("You selected: Add bank transaction")
            bank_name, destination, amount = get_bank_transaction_detail()
            data.move_funds_from_bank(bank_name, destination, amount)

        case "9":
            print("You selected: Work with existing output")
            data.open_existing_data()
        case "0":
            print("Generating Visualization. . .")
            data.generate()

            break
        case _:
            print("Invalid choice. Please try again.")

print("Thank you for using this app.")
filename = "output.json"
print(f"Cashflow data generated in {os.path.join(os.getcwd(), filename)}")
