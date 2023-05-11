# Storygraph-Gantt-Chart-Generator
Use your [Storygraph](https://app.thestorygraph.com/) reading journal to create a timeline of books you have read.

From your Storygraph, click on your profile at the top right, then **'Manage Account'** -> **'Manage Your Data'** -> **'Export Storygraph Library'**. This will allow you to download a CSV containing all books you have logged on the site which you can use to generate a timeline of the books you've read.

## Quick Usage
```sh
python ChartGenerator -i storygraph_export.csv -o mychart.png
```

creates a chart like:

![This was the first chart I made lol](https://i.imgur.com/KhfGfqN.png)

Disclaimer: I am not affiliated with or endorsed by The Storygraph in any way.
