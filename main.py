import os
from src.flow import GenerateDataset

data = GenerateDataset()
heading = """

   _______   _  ____ ________  __  __________  __
  / __/ _ | / |/ / //_/ __/\ \/ / / ___/ __/ |/ /
 _\ \/ __ |/    / ,< / _/   \  / / (_ / _//    /
/___/_/ |_/_/|_/_/|_/___/   /_/  \___/___/_/|_/


"""

print(heading)
print("Visualize Entity Flow!!")


def get_input():
    name = input(f"Name: ")
    value = input(f"Value: ")
    return name, value


def get_flow_details():
    bank_name = input(f"Source Name: ")
    destination = input(f"Target Name: ")
    amount = input(f"Value: ")
    return bank_name, destination, amount


while True:
    raw_input = input(
        "Menu:\n"
        "[1] Add Source\n"
        "[2] Add Flow\n"
        "[9] Work with existing output\n"
        "[0] Vizualize flow\n\n"
        "Enter your choice: "
    )

    match raw_input:
        case "1":
            print("You selected: Add Source")
            name, value = get_input()
            data.add_source(name, value)
            print("\n Source successfully added!\n")
        case "2":
            print("You selected: Add Flow")
            source, target, value = get_flow_details()
            data.add_flow(source, target, value)
            print("\n Flow successfully added!\n")
        case "9":
            print("You selected: Work with existing output")
            data.open_existing_data()
        case "0":
            print("Generating Visualization. . .")
            data.generate()

            break
        case _:
            print("Invalid choice. Please try again.")

filename = "output.json"
print(f"Flow data generated in {os.path.join(os.getcwd(), filename)}")
