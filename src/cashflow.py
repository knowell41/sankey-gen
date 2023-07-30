import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
import json
import os


class GenerateDataset:
    INCOME = {}
    SAVINGS = {}
    EXPENSES = {}
    BANKS = {}
    BANK_TRANSACTIONS = {}
    existing_data = {}

    def __init__(self) -> None:
        pass

    def move_funds_from_bank(self, bank_name, transaction_name, value):
        bank_name = bank_name.strip().lower()
        transaction_name = transaction_name.strip().lower()
        try:
            self.BANK_TRANSACTIONS[bank_name] = [transaction_name, int(value)]
        except ValueError:
            print("Failed to define income. Floating values only.")

    def add_bank(self, name, value):
        name = name.strip().lower()
        try:
            self.BANKS[name] = int(value)
        except ValueError:
            print("Failed to define income. Floating values only.")

    def add_income(self, name, value):
        name = name.strip().lower()
        try:
            self.INCOME[name] = int(value)
        except ValueError:
            print("Failed to define income. Floating values only.")

    def add_expenses(self, name, value):
        name = name.strip().lower()
        try:
            self.EXPENSES[name] = int(value)
        except ValueError:
            print("Failed to define income. Floating values only.")

    def add_savings(self, name, value):
        try:
            self.SAVINGS[name] = int(value)
        except ValueError:
            print("Failed to define income. Floating values only.")

    def open_existing_data(self):
        file = os.path.join(os.getcwd(), "output.json")

        with open(file, "r") as datafile:
            self.existing_data = json.load(datafile)

    def _display(self, data):
        data = data.fillna("none")
        categories = data["source"].unique().tolist() + ["none"]
        data = data.to_dict(orient="records")

        with open("output.json", "w") as outfile:
            json.dump(data, outfile)

        links = []
        for d in data:
            links.append(
                {
                    "source": categories.index(d["source"]),
                    "target": categories.index(d["target"]),
                    "value": d["value"],
                }
            )

        # Create the Sankey diagram
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=categories,
                    ),
                    link=dict(
                        source=[link["source"] for link in links],
                        target=[link["target"] for link in links],
                        value=[link["value"] for link in links],
                    ),
                )
            ]
        )

        # Update layout settings
        fig.update_layout(title_text="Sample Sankey Diagram", font_size=10)

        # Show the plot
        fig.show()

    def generate(self):
        data = []
        income_total = 0
        expenses_total = 0
        savings_total = 0
        for k, v in self.INCOME.items():
            new_record = {"source": k, "target": "income", "value": v}
            data.append(new_record)
            income_total += v
        for k, v in self.EXPENSES.items():
            new_record = {"source": "income", "target": k, "value": v}
            data.append(new_record)
            expenses_total += v
        for k, v in self.SAVINGS.items():
            new_record = {"source": "income", "target": k, "value": v}
            data.append(new_record)
            savings_total += v
        for k, v in self.BANKS.items():
            new_record = {"source": "income", "target": k, "value": v}
            data.append(new_record)

        for k, v in self.BANK_TRANSACTIONS.items():
            new_record = {"source": k, "target": v[0], "value": v[1]}
            data.append(new_record)

        if self.existing_data:
            data += self.existing_data

        data_df = pd.DataFrame(data)
        unique_sources = data_df["source"].unique().tolist()
        unique_target = data_df["target"].unique().tolist()
        unique_names = list(set(unique_sources + unique_target))
        delta_names = list(set(unique_target) - set(unique_sources))
        for name in delta_names:
            data.append(
                {"source": name, "target": None, "value": 0, "node_label": None}
            )
        data_df = pd.DataFrame(data)
        # print(data_df)
        self._display(data_df)
