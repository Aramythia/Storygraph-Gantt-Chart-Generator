import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import datetime as dt
import sys

PATH = sys.argv[1]

df = pd.read_csv(PATH, usecols=("Title", "Authors", "Dates Read"))

# Clean up data to have only ranged dates
df = df[df["Dates Read"].map(lambda x : x is not np.nan)]
df = df[df["Dates Read"].map(lambda x : len(x.split('-')) == 2)]

# Separate dates into their own columns
df["start_date"] = df["Dates Read"].map(lambda x : x.split('-')[0])
df["end_date"] = df["Dates Read"].map(lambda x : x.split('-')[1])

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

df.sort_values(by="start_date", ascending=False, inplace=True)

# Get a new title column
df["Title"] = df["Title"] + " (" + df["Authors"] + ")"
df.drop(["Authors", "Dates Read"], inplace=True, axis=1)

# Auxiliary Columns
first_month = df["start_date"].min().replace(day=1)

df["days_to_start"] = (df["start_date"] - df["start_date"].min()).dt.days
df["days_to_end"] = (df["end_date"] - df["start_date"].min()).dt.days
df["elapsed"] = df["days_to_end"] - df["days_to_start"] + 1

# Chart
fig, ax = plt.subplots()

plt.barh(y=df["Title"], width=df["elapsed"], left=df["days_to_start"])
plt.title("Book Timeline")
ax.xaxis.grid(True, alpha=0.5)

# Add labels to the chart
xticks = np.arange(0, df["days_to_end"].max(), 14)
xlabels = pd.date_range(df["start_date"].min(), df["end_date"].max()).strftime("%d %b %y")[::14]

ax.set_xticks(xticks)
ax.set_xticklabels(xlabels, rotation=60, ha="right")

plt.show()
