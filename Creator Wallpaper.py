import ctypes
import os
import tkinter as tk

from PIL import ImageTk
from PIL import Image

from data.data import recover_images, select_image, remove_select_image, \
    get_number_select_image

def set_wallpaper(img):
    images = img
    path_os = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{path_os}\wallpaper\{images}", 0)
    print('The wallpaper was well changed !')

class Select_Interface(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(Select_Interface, self).__init__()

        self.save_selection = []
        self.i = None
        self.value = None
        self.images = []

        self.geometry("1200x720")
        self.config(background="#1C1C1C")
        self.title("One day, One image | Creator Wallpaper")
        self.iconbitmap('./LOGO APP/logo.ico')
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

        self.canva = tk.Canvas(self, width=1000, height=0.01)
        self.canva.place(x=0, y=580)

        path = os.getcwd()
        path_img = f'{path}/LOGO APP/nasa.png'
        img = Image.open(path_img)
        Images = img.resize((558, 720), Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(Images)
        self.add_picture = tk.Label(self, image=picture, bd=0)
        self.add_picture.pack(side=tk.RIGHT)

        picture_btn_selection = tk.PhotoImage(file=r"LOGO APP/button/selection_btn.png").subsample(2)
        self.select_button = tk.Button(self, image=picture_btn_selection, bg="#1C1C1C", fg="white", activebackground="#1C1C1C",
                                       activeforeground="white", font=('arial', 20, 'bold'), bd=0, command=self.get_value)
        self.select_button.pack(pady=300)

        picture_btn_create = tk.PhotoImage(file=r"LOGO APP/button/create_btn.png").subsample(3)
        btn_create = tk.Button(self, image=picture_btn_create, bg="#1C1C1C", bd=0, activebackground='#1C1C1C', command=self.set_wallpaper)
        btn_create.place(x=50, y=600)

        picture_btn_preview = tk.PhotoImage(file=r"LOGO APP/button/preview_btn.png").subsample(3)
        btn_preview = tk.Button(self, image=picture_btn_preview, bg="#1C1C1C", bd=0, activebackground='#1C1C1C', command=self.preview_img)
        btn_preview.place(x=380, y=600)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()

    def on_closing(self):
        remove_select_image()
        self.destroy()

    def get_value(self):
        value_select = self.select_images.get(tk.ACTIVE)
        self.save_selection.append(value_select)

        for item in range(len(self.save_selection)):

            if " ✓" not in value_select:
                select_image(value_select)
                self.images.append(f'./image/{value_select}')
            if get_number_select_image() > 6:
                print("You can't choose more than 6 images !")
                break
            else:
                characters = ' ✓'
                for x in range(len(characters)):
                    count = self.select_images.index(tk.ACTIVE)
                    self.select_images.delete(count)

                    if " ✓" in value_select:
                        self.select_images.insert(count, f"{value_select}")
                    else:
                        self.select_images.insert(count, f"{value_select} ✓")
                    return value_select, self.save_selection

    def select(self, event):
        characters = ' ✓'
        for x in range(len(characters)):
            widget = event.widget
            selection = widget.curselection()
            string = widget.get(selection)
            self.value = string.replace(characters[x], "")

        # - Change image - #

        path = os.getcwd()
        path_img = f'{path}/image/{self.value}'
        img = Image.open(path_img)
        Images = img.resize((558, 720), Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(Images)
        self.add_picture.photo = picture
        self.add_picture['image'] = picture

    def create_img(self):
        image = [Image.open(x) for x in self.images]
        total_width = 0
        max_height = 0
        for img in image:
            total_width += img.size[0]
            max_height = max(max_height, img.size[1])

        wallpaper_created = Image.new('RGB', (total_width, max_height))
        current_width = 0

        for img in image:
            wallpaper_created.paste(img, (current_width, 0))
            current_width += img.size[0]

        wallpaper_created.save('./wallpaper/YourWallpaper.jpg')

    def set_wallpaper(self):
        self.create_img()
        set_wallpaper('YourWallpaper.jpg')

    def preview_img(self):
        self.create_img()
        windows = tk.Tk()
        path_img = f'./wallpaper/YourWallpaper.jpg'
        img = Image.open(path_img)
        windows.geometry(f'{img.size[0]}x{img.size[1]}')
        windows.title(f"Preview : YourWallpaper.jpg | Taille : {img.size[0]}x{img.size[1]}")
        windows.iconbitmap('./LOGO APP/preview_icon.ico')
        image = ImageTk.PhotoImage(img, master=windows)
        display_img = tk.Label(windows, image=image)
        display_img.photo = image
        display_img.pack()
        windows.resizable(False, False)
        windows.mainloop()

Select_Interface()
