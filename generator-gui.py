import PIL.Image, PIL.ImageTk

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from ChartGenerator import ChartGenerator

class ImageFrame(ttk.Frame):
    def __init__(self, container, image):
        super().__init__(container)

        # self.image = image
        self.original_image = image
        self.image = PIL.ImageTk.PhotoImage(image)

        self.label = ttk.Label(self, image=self.image)
        self.label.grid(column=0, row=0, sticky='w')

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

class ControlFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self['text'] = "Options"

        self.input_button = ttk.Button(self, text="Upload CSV", command=self.upload_csv)
        self.input_button.grid(column=0, row=1, sticky=W)

        self.grid(column=0, row=1, padx=5, pady=5, sticky="ew")

    def upload_csv(self):
        filename = filedialog.askopenfilename(filetypes=(("csv files", "*.csv"),))

        image = ChartGenerator(filename).get_image()

        self.display = ImageFrame(self.container, image)

        self.save_button = ttk.Button(self, text="Save", command=self.save_image)
        self.save_button.grid(column=1, row=1, sticky=W)

    def save_image(self):
        directory = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=(("png files", "*.png"),),
            defaultextension=".png")
        
        if directory == "":
            return
        else:
            self.display.original_image.save(directory, format="png")

def main():
    root = Tk()
    root.title = "Book Timeline"

    ControlFrame(root)

    root.mainloop()


if __name__ == "__main__":
    main()