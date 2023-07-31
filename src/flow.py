import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
import json
import os
from datetime import datetime


class GenerateDataset:
    SOURCE = {}
    FLOW = {}
    existing_data = {}

    def __init__(self) -> None:
        pass

    def add_flow(self, source_name, target_name, value):
        source_name = source_name.strip().upper()
        target_name = target_name.strip().upper()
        try:
            self.FLOW[source_name] = [target_name, int(value)]
        except ValueError:
            print("Failed to add flow. Floating/integer values only.e.g 1.00")

    def add_source(self, source_name, value):
        source_name = source_name.strip().upper()
        try:
            self.SOURCE[source_name] = int(value)
        except ValueError:
            print("Failed to define source. Floating/integer values only. e.g 1.00 ")

    def open_existing_data(self):
        file = os.path.join(os.getcwd(), "temp.json")

        with open(file, "r") as datafile:
            self.existing_data = json.load(datafile)

    def _display(self, data):
        data = data.fillna("none")
        categories = data["source"].unique().tolist() + ["none"]
        data = data.to_dict(orient="records")

        now = datetime.now().strftime("%d%m%y-%H%M%S")
        output_filename = f"output/{now}.json"
        with open(output_filename, "w") as outfile:
            json.dump(data, outfile)

        with open("temp.json", "w") as outfile:
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
        for k, v in self.SOURCE.items():
            new_record = {"source": "principal", "target": k, "value": v}
            data.append(new_record)
            income_total += v

        for k, v in self.FLOW.items():
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
        self._display(data_df)
