import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import datetime as dt

PATH = r"C:\Users\sebas\Downloads\f6f2324351b7e56ff64a5504d251c7a93d10c531d820363e713d5f3502b5442f.csv"

# DATA RETRIEVAL AND SANITIZATION
df = pd.read_csv(PATH, usecols=("Title", "Authors", "Read Status", "Dates Read"))
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
plt.title("Book Timeline")

ax.xaxis.grid(True, alpha=0.5)
dates = pd.date_range(df["start"].min(), df["end"].max(), freq="SMS")
ax.set_xticks(dates)
ax.set_xticklabels(dates.strftime("%d %b %y"), rotation=45)

ax.barh(y=df["title"], width=df["elapsed"], left=df["start"])

plt.savefig("img.png", bbox_inches="tight")