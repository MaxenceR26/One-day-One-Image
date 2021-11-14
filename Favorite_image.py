import os
import tkinter as tk

from PIL import ImageTk
from PIL import Image
import PIL.Image as pl

from data.data import recover_images, count_json, select_image, get_select_image, remove_select_image


class Select_Interface(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(Select_Interface, self).__init__()

        self.save_selection = []
        self.i = None

        self.geometry("1200x720")
        self.config(background="#1C1C1C")
        self.resizable(False, False)

        frame = tk.Frame(self)

        yDefilB = tk.Scrollbar(frame, orient='vertical')
        yDefilB.grid(row=0, column=1, sticky='ns')

        self.select_images = tk.Listbox(frame)
        self.select_images.grid(row=0, column=1, sticky='ns')

        self.select_images.config(background="#3A3A3A", highlightcolor="red",
                                  highlightthickness=0, selectbackground="#1C1C1C",
                                  fg='white', border=1, xscrollcommand=yDefilB, width=80)

        self.select_images.configure(justify=tk.CENTER)

        yDefilB['command'] = self.select_images.yview
        self.select_images.bind("<Double-Button-1>", self.select)
        self.select_images.insert(0, *recover_images())

        frame.place(x=0, y=0)
        

        path = os.getcwd()
        path_img = f'{path}/LOGO APP/nasa.png'
        img = Image.open(path_img)
        Images = img.resize((558, 720), Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(Images)
        self.add_picture = tk.Label(self, image=picture, bd=0)
        self.add_picture.pack(side=tk.RIGHT)

        self.select_button = tk.Button(self, text="Selection", bg="#1C1C1C", fg="white", activebackground="#1C1C1C", activeforeground="white", font=('arial', 20,'bold'), command=self.get_value)
        self.select_button.pack(pady=240)

        self.look_selection = tk.Label(self,
                                  text=f"")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()

    def on_closing(self):
        remove_select_image()
        print(get_select_image())
        self.destroy()

    def get_value(self):
        value_select = self.select_images.get(tk.ACTIVE)
        # print(value_select)
        self.save_selection.append(value_select)
        for item in range(len(self.save_selection)):

            # self.i = item
            # print(self.save_selection[item])
            select_image(value_select)
            self.look_selection.place(x=100, y=200)
            if len(self.save_selection) > 6:
                print("Tu ne peux pas choisir plus de 6 images !")
            else:
                if len(self.save_selection) > 1:
                    self.look_selection['text'] = f"Tu as choisi {len(self.save_selection)} images : \n {get_select_image()}"
                else:
                    self.look_selection[
                        'text'] = f"Tu as choisi {len(self.save_selection)} image : \n {value_select}"

        # print(self.save_selection[self.i])


    def select(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection)

        # - Change image - #

        path = os.getcwd()
        path_img = f'{path}/image/{value}'
        img = Image.open(path_img)
        Images = img.resize((558, 720), Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(Images)
        self.add_picture.photo = picture
        self.add_picture['image'] = picture


Select_Interface()
