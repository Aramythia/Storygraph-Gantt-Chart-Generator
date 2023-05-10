"""
PROBLEMS WITH STORYGRAPH DATA

The only way to retrieve StoryGraph data at this time is by manually exporting 
    it on the website. This means user-input to this program.
The real issue is that the data comes in a .csv with little data validation and 
    awkward formatting. Sanitization is necessary.
The significant fields of the Storygraph CSV are:
    Title: str 
    Authors: str (multiple authors separated by commas)
    Read Status: str (either 'read', 'to-read', or 'currently-reading' afaik)
    Dates Read: mm/dd/yyyy-mm/dd/yyyy; the range of dates the book was logged 
        as 'currently-reading'
        Sometimes only one date is listed. If the book has been read multiple 
            times, the ranges are comma-separated
    Rating: numeric; the user's rating for the book (maybe I can find a way to 
        implement this into the chart)
        
One roadblock to a simple program is that there is too much user-defined data to 
parse in a consistent way. After examination of my own data, only the 'Dates Read'
field can reliably be used to gain the reading dates of a book, but this field 
has some problems:
1. The mm/dd/yyyy-mm/dd/yyyy format actually isn't there in every case.
    I can edit my user-data. I can delete my start-date and/or end-date of the 
    books which I have read. Then the csv will only list the dates it has. 
    Likewise I also backfilled my account with a bunch of books I had read
    before I created my Storygraph account. I forgot the exact dates I had 
    read them, so I left those fields blank, leading to the same issue. 
    Unfortunately, the data isn't there, so such cases cannot be included in 
    the chart. 
2. 'Dates Read' is empty for books being currently read.
3. The format is actually "mm/dd/yyyy-mm/dd/yyyy"*N, where N is the amount of
    times I have read the book. 
    This isn't a catastrophic issue, but actually a good thing. This means, 
    however, another challenge to creating the chart, and requires a different
    way of thinking about the data which considers how to display book rereads.
Issue 3 actually broke my original script. I reread a book that I had read
    before creating the account, so not only did I have a csv-list thingy to 
    deal with, but also a hanging date (I forgot the start date to the first
    reading session). The base pandas parser freaked out when it saw that.
"""

import pandas as pd
import numpy as np

import matplotlib
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