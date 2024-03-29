import argparse
from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from PIL import Image

from io import BytesIO
import datetime as dt

class ChartGenerator():
    def __init__(self, input_file : Path):
        self.input_file = input_file

        # DATA RETRIEVAL AND SANITIZATION
        df = pd.read_csv(self.input_file, 
            usecols=("Title", "Authors", "Read Status", "Dates Read"))
        df = df.loc[df['Read Status'] == "read"]
        df.drop(["Read Status"], inplace=True, axis=1)

        df.columns = ["title", "authors", "range"] # shorten colnames for my sanity

        df['range'] = df['range'].map(lambda x : x.split(","))
        data = []
        parse_date = lambda date : dt.datetime.strptime(date, "%Y/%m/%d").date()
        for i, row in df.iterrows():
            for range in row['range']: # Create a separate row for each reading session
                date_list = [date.strip() for date in range.split('-')]
                if len(date_list) == 2: # Then its in date-date format (only valid case)
                    data.append({
                        "title" : row['title'],
                        "authors" : row['authors'],
                        "start" : parse_date(date_list[0]),
                        "end" : parse_date(date_list[1])
                    })
        data.sort(key=lambda x : x['start'])

        df = pd.DataFrame(data)

        # # CALCULATIONS AND PLOTTING
        df["elapsed"] = df["end"] - df["start"] + dt.timedelta(days=1)

        fig, ax = plt.subplots()
        ax.set_title("Book Timeline")

        ax.xaxis.grid(True, alpha=0.5)
        dates = pd.date_range(df["start"].min(), df["end"].max(), freq="SMS")
        ax.set_xticks(dates)
        ax.set_xticklabels(dates.strftime("%d %b %y"), rotation=45)

        ax.barh(y=df["title"], width=df["elapsed"], left=df["start"])

        self.figure = { "fig" : fig, "ax" : ax }

    def get_image(self):
        buf = BytesIO()
        self.figure['fig'].savefig(buf, bbox_inches="tight")
        buf.seek(0)
        return Image.open(buf)
    
    def save_image(self, output_file):
        self.figure['fig'].savefig(output_file, bbox_inches="tight")


def main(input_file : Path, output_file : Path):
    ChartGenerator(input_file).save_image(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", type=Path, required=True)
    parser.add_argument("-o", "--output_file", type=Path, required=True)

    args = parser.parse_args()

    main(**args.__dict__)