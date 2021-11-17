# Project realized by Maxence R.
# Fan of Space !
# Love Nasa

# Import Module

import tkinter
from datetime import date, timedelta
import requests
import os
from pathlib import Path
import wget
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from requests import get
import PIL.Image as pl
import ctypes


from data.data import recv_token, recv_image, _add_favoris, _remove_favoris


def ScrapImage(url: str = None) -> None:
    i = wget.detect_filename(url)
    path = Path(f'.\image\{i}')
    if path.exists():
        os.remove(f'.\image\{i}')

    wget.download(url, 'image')


def ScrapColor_Img(url: str = None) -> None:
    i = wget.detect_filename(url)

    image = pl.open(f'.\image\{i}')
    x = 3
    y = 10
    (red, green, blue) = image.getpixel((x, y))
    Main(red, green, blue, i)


def _rgb(rgb):
    return "#%02x%02x%02x" % rgb


def set_wallpaper(img):
    images = img
    path_os = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{path_os}\image\{images}", 0)
    print('The wallpaper was well changed !')


def get_today():
    dates = date.today()
    return dates


def get_day(n: int = None) -> date:
    dates = date.today() - timedelta(days=n)
    return dates


class Main(tk.Tk):
    def __init__(self, r: str = None, g: str = None, b: str = None, name_picture: str = None):
        super().__init__()
        request = get(
            f'https://api.nasa.gov/planetary/apod?api_key={recv_token()}')
        data = request.json()
        self.name_picture = name_picture
        path_img = f'./image/{self.name_picture}'

        self.config(background=_rgb((r, g, b)))
        self.geometry('1400x720')
        self.title(f'{self.name_picture} | Informations | One Day, One Image ! NASA')
        self.iconbitmap('./LOGO APP/logo.ico')
        self.resizable(False, False)

        self.img = Image.open(path_img)
        self.Images = self.img.resize((558, 720), Image.ANTIALIAS)
        self.Images = ImageTk.PhotoImage(self.Images)
        self.Picture = tk.Label(self, image=self.Images, bd=0, bg='white')
        self.Picture.pack(side=tk.LEFT)

        self.Title = tk.Label(self, text=f"\n{data['title']}", bg=_rgb((r, g, b)), fg='white',
                              font=('Arial', 16, 'bold'))
        self.Title.pack()

        try:
            self.Author = tk.Label(self, text=f"\nAuthor: {data['copyright']}", bg=_rgb((r, g, b)), fg='white',
                                   font=('Arial', 11))
            self.Author.pack()
        except KeyError as e:
            self.Author = tk.Label(self, text=f"\nAuthor: None", bg=_rgb((r, g, b)), fg='white',
                                   font=('Arial', 11))
            self.Author.pack()

        self.Date_picture = tk.Label(self, text=f"Date of picture: {data['date']}", bg=_rgb((r, g, b)), fg='white',
                                     font=('Arial', 11))
        self.Date_picture.pack()

        self.add_favoris_text = tk.Label(self, text=f"Add Favoris :", bg=_rgb((r, g, b)), fg='white',
                                     font=('Arial', 10, 'bold'))
        self.add_favoris_text.place(x=922, y=635)

        self.explanation_text = f"Explanation:\n\n{data['explanation']}"

        self.explanation = tkinter.Text(self, height=15)
        self.explanation.insert(tk.END, self.explanation_text)
        self.explanation.config(state='disabled', bg=_rgb((r, g, b)), fg='white', font=('Arial', 11), bd=0)
        self.explanation.tag_add("tag_center", '1.0')
        self.explanation.tag_configure("tag_center", justify='center')

        self.explanation.pack()

        self.wallpaper_btn = tk.Button(self, text="Set like Wallpaper", bd=0,
                                       bg=_rgb((int(r) + 20, int(g) + 20, int(b) + 20)), fg='white',
                                       font=('Arial', 11, 'bold'),
                                       activebackground=_rgb((int(r) + 20, int(g) + 20, int(b) + 20)),
                                       activeforeground='white',
                                       height=4,
                                       command=lambda: set_wallpaper(self.name_picture))
        self.wallpaper_btn.pack()

        self.canva = tk.Canvas(self, width=1500, height=0.1)
        self.canva.place(x=558, y=615)

        self.options_list = ["Yesterday", "3 days", "7 days"]
        self.value_inside = tkinter.StringVar(self)
        self.value_inside.set("Select an choice")
        self.select_menu = tkinter.OptionMenu(self, self.value_inside, *self.options_list,
                                              command=self.display_selected_menu)
        self.select_menu.place(x=620, y=660)
        self.select_menu['highlightthickness'] = 0
        self.select_menu['border'] = 0
        self.select_menu['justify'] = 'center'
        self.select_menu['bg'] = _rgb((int(r) + 70, int(g) + 70, int(b) + 70))
        self.select_menu['activebackground'] = _rgb((int(r) + 70, int(g) + 70, int(b) + 70))
        self.select_menu['fg'] = 'white'
        self.select_menu['activeforeground'] = 'white'

        self.select_var = tk.StringVar()
        self.select_entry = tk.Entry(self, textvariable=self.select_var)
        self.select_entry['highlightthickness'] = 0
        self.select_entry['border'] = 0
        self.select_entry['justify'] = 'center'
        self.select_entry['bg'] = _rgb((int(r) + 70, int(g) + 70, int(b) + 70))
        self.select_entry['fg'] = 'white'

        self.select_entry.insert(0, f'Exemple : {get_today()}')
        self.select_entry.bind('<Return>', self.enter)
        self.select_entry.place(x=1175, y=660, height=30)

        self.date_to_see = tk.Label(self, text=f"Date to see :", bg=_rgb((r, g, b)), fg='white')
        self.date_to_see.place(x=1210, y=630)

        Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
        self.favoris_btn = tk.Button(self, image=Images, bg=_rgb((r, g, b)), activebackground=_rgb((r, g, b)), bd=0, command=self.favoris_setup)
        self.favoris_btn.pack(side=tk.BOTTOM, pady=23)

        if self.name_picture in recv_image():
            Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
            self.favoris_btn.photo = Images
            self.favoris_btn['image'] = Images
        else:
            Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
            self.favoris_btn.photo = Images
            self.favoris_btn['image'] = Images

        self.count = 0

        self.mainloop()

    def favoris_setup(self):
        self.count += 1
        if self.count == 1:
            Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
            self.favoris_btn.photo = Images
            self.favoris_btn['image'] = Images
            _add_favoris(self.name_picture)
            self.count += 1

        elif self.count >= 2:
            Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
            self.favoris_btn.photo = Images
            self.favoris_btn['image'] = Images
            _remove_favoris(self.name_picture)
            self.count -= self.count

        return self.count

    def enter(self, event=None):
        date = self.select_entry.get()
        request = get(
            f'https://api.nasa.gov/planetary/apod?api_key={recv_token()}&date={date}')
        response = request.json()

        if response['media_type'].lower()[0:5] == 'image':
            url = response['url']
            ScrapImage(url)
            self.name_picture = wget.detect_filename(url)
            self.title(f"{response['title']}.jpg | Informations | One Day, One Image ! NASA")
            path = os.getcwd()
            path_img = f'{path}/image/{self.name_picture}'
            img = Image.open(path_img)
            Images = img.resize((558, 720), Image.ANTIALIAS)
            Images = ImageTk.PhotoImage(Images)
            self.Picture.photo = Images
            self.Picture['image'] = Images

            # Scrap color img for here

            i = wget.detect_filename(url)

            image = pl.open(f'.\image\{i}')
            x = 3
            y = 10
            (red, green, blue) = image.getpixel((x, y))

            self.config(background=_rgb((red, green, blue)))
            self.Title['bg'] = _rgb((red, green, blue))
            self.Author['bg'] = _rgb((red, green, blue))
            self.Date_picture['bg'] = _rgb((red, green, blue))
            self.Date_picture['bg'] = _rgb((red, green, blue))
            self.explanation['bg'] = _rgb((red, green, blue))
            self.select_menu['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
            self.select_entry['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
            self.date_to_see['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
            self.wallpaper_btn['bg'] = _rgb((int(red) + 20, int(green) + 20, int(blue) + 20))
            self.favoris_btn['bg'] = _rgb((red, green, blue))
            self.favoris_btn.config(activebackground=_rgb((red, green, blue)))

            # Changing text

            self.Title['text'] = response['title']
            try:
                self.Author['text'] = f"\nAuthor: {response['copyright']}"
            except KeyError as e:
                self.Author['text'] = f"\nAuthor: None"
            self.Date_picture['text'] = f"Date of picture: {response['date']}"

            explanations_text = f"Explanation:\n\n{response['explanation']}"
            self.explanation['state'] = 'normal'
            self.explanation.delete('1.0', tk.END)
            self.explanation.insert(tk.END, explanations_text)
            self.explanation['state'] = 'disabled'
            self.explanation.tag_add("tag_center", '1.0')
            self.explanation.tag_configure("tag_center", justify='center')


            # Changing button set image wallpaper

            self.wallpaper_btn['command'] = lambda: set_wallpaper(self.name_picture)

            if self.name_picture in recv_image():
                Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
                self.favoris_btn.photo = Images
                self.favoris_btn['image'] = Images
            else:
                Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
                self.favoris_btn.photo = Images
                self.favoris_btn['image'] = Images

        else:
            print(
                f"/!\ Unfortunately, on this day, NASA to publish {response['media_type']} is not an image! Try tomorrow :)")
            if response['media_type'].lower()[0:5] == 'video':
                print('\nIf you want to see the video :\n'
                      f"URL : {response['url']}")

    def display_selected_menu(self, *args, **kwargs) -> None:
        get_value = self.value_inside.get()
        if get_value == "Yesterday":
            request = get(
                f'https://api.nasa.gov/planetary/apod?api_key={recv_token()}&date={get_day(1)}')
            response = request.json()

            if response['media_type'].lower()[0:5] == 'image':
                url = response['url']
                ScrapImage(url)
                self.name_picture = wget.detect_filename(url)
                self.title(f"{response['title']}.jpg | Informations | One Day, One Image ! NASA")
                path = os.getcwd()
                path_img = f'{path}/image/{self.name_picture}'
                img = Image.open(path_img)
                Images = img.resize((558, 720), Image.ANTIALIAS)
                Images = ImageTk.PhotoImage(Images)
                self.Picture.photo = Images
                self.Picture['image'] = Images

                # Scrap color img for here

                i = wget.detect_filename(url)

                image = pl.open(f'.\image\{i}')
                x = 3
                y = 10
                (red, green, blue) = image.getpixel((x, y))

                self.config(background=_rgb((red, green, blue)))
                self.Title['bg'] = _rgb((red, green, blue))
                self.Author['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.explanation['bg'] = _rgb((red, green, blue))
                self.select_menu['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.select_entry['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.date_to_see['bg'] = _rgb((red, green, blue))
                self.wallpaper_btn['bg'] = _rgb((int(red) + 20, int(green) + 20, int(blue) + 20))
                self.favoris_btn['bg'] = _rgb((red, green, blue))
                self.favoris_btn.config(activebackground=_rgb((red, green, blue)))
                # Changing text

                self.Title['text'] = response['title']
                try:
                    self.Author['text'] = f"\nAuthor: {response['copyright']}"
                except KeyError as e:
                    self.Author['text'] = f"\nAuthor: None"
                self.Date_picture['text'] = f"Date of picture: {response['date']}"

                explanations_text = f"Explanation:\n\n{response['explanation']}"
                self.explanation['state'] = 'normal'
                self.explanation.delete('1.0', tk.END)
                self.explanation.insert(tk.END, explanations_text)
                self.explanation['state'] = 'disabled'
                self.explanation.tag_add("tag_center", '1.0')
                self.explanation.tag_configure("tag_center", justify='center')

                # Changing button set image wallpaper

                self.wallpaper_btn['command'] = lambda: set_wallpaper(self.name_picture)

                if self.name_picture in recv_image():
                    Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
                else:
                    Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
            else:
                print(
                    f"/!\ Unfortunately, on this day, NASA to publish {response['media_type']} is not an image! Try tomorrow :)")
                if response['media_type'].lower()[0:5] == 'video':
                    print('\nIf you want to see the video :\n'
                          f"URL : {response['url']}")

        if get_value == "3 days":
            request = get(
                f'https://api.nasa.gov/planetary/apod?api_key={recv_token()}&date={get_day(3)}')
            response = request.json()

            if response['media_type'].lower()[0:5] == 'image':
                url = response['url']
                ScrapImage(url)
                self.name_picture = wget.detect_filename(url)
                self.title(f"{response['title']}.jpg | Informations | One Day, One Image ! NASA")
                path = os.getcwd()
                path_img = f'{path}/image/{self.name_picture}'
                img = Image.open(path_img)
                Images = img.resize((558, 720), Image.ANTIALIAS)
                Images = ImageTk.PhotoImage(Images)
                self.Picture.photo = Images
                self.Picture['image'] = Images

                # Scrap color img for here

                i = wget.detect_filename(url)

                image = pl.open(f'.\image\{i}')
                x = 3
                y = 10
                (red, green, blue) = image.getpixel((x, y))

                self.config(background=_rgb((red, green, blue)))
                self.Title['bg'] = _rgb((red, green, blue))
                self.Author['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.explanation['bg'] = _rgb((red, green, blue))
                self.select_menu['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.select_entry['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.date_to_see['bg'] = _rgb((red, green, blue))
                self.wallpaper_btn['bg'] = _rgb((int(red) + 20, int(green) + 20, int(blue) + 20))
                self.favoris_btn['bg'] = _rgb((red, green, blue))
                self.favoris_btn.config(activebackground=_rgb((red, green, blue)))
                # Changing text

                self.Title['text'] = response['title']
                try:
                    self.Author['text'] = f"\nAuthor: {response['copyright']}"
                except KeyError as e:
                    self.Author['text'] = f"\nAuthor: None"
                self.Date_picture['text'] = f"Date of picture: {response['date']}"

                explanations_text = f"Explanation:\n\n{response['explanation']}"
                self.explanation['state'] = 'normal'
                self.explanation.delete('1.0', tk.END)
                self.explanation.insert(tk.END, explanations_text)
                self.explanation['state'] = 'disabled'
                self.explanation.tag_add("tag_center", '1.0')
                self.explanation.tag_configure("tag_center", justify='center')

                # Changing button set image wallpaper

                self.wallpaper_btn['command'] = lambda: set_wallpaper(self.name_picture)

                if self.name_picture in recv_image():
                    Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
                else:
                    Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
            else:
                print(
                    f"/!\ Unfortunately, on this day, NASA to publish {response['media_type']} is not an image! Try tomorrow :)")
                if response['media_type'].lower()[0:5] == 'video':
                    print('\nIf you want to see the video :\n'
                          f"URL : {response['url']}")
        if get_value == "7 days":
            request = get(
                f'https://api.nasa.gov/planetary/apod?api_key={recv_token()}&date={get_day(7)}')
            response = request.json()

            if response['media_type'].lower()[0:5] == 'image':
                url = response['url']
                ScrapImage(url)
                self.name_picture = wget.detect_filename(url)
                self.title(f"{response['title']}.jpg | Informations | One Day, One Image ! NASA")
                path = os.getcwd()
                path_img = f'{path}/image/{self.name_picture}'
                img = Image.open(path_img)
                Images = img.resize((558, 720), Image.ANTIALIAS)
                Images = ImageTk.PhotoImage(Images)
                self.Picture.photo = Images
                self.Picture['image'] = Images

                # Scrap color img for here

                i = wget.detect_filename(url)

                image = pl.open(f'.\image\{i}')
                x = 3
                y = 10
                (red, green, blue) = image.getpixel((x, y))

                self.config(background=_rgb((red, green, blue)))
                self.Title['bg'] = _rgb((red, green, blue))
                self.Author['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.Date_picture['bg'] = _rgb((red, green, blue))
                self.explanation['bg'] = _rgb((red, green, blue))
                self.select_menu['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.select_entry['bg'] = _rgb((int(red) + 70, int(green) + 70, int(blue) + 70))
                self.date_to_see['bg'] = _rgb((red, green, blue))
                self.wallpaper_btn['bg'] = _rgb((int(red) + 20, int(green) + 20, int(blue) + 20))
                self.favoris_btn['bg'] = _rgb((red, green, blue))
                self.favoris_btn.config(activebackground=_rgb((red, green, blue)))

                # Changing text

                self.Title['text'] = response['title']
                try:
                    self.Author['text'] = f"\nAuthor: {response['copyright']}"
                except KeyError as e:
                    self.Author['text'] = f"\nAuthor: None"

                self.Date_picture['text'] = f"Date of picture: {response['date']}"

                explanations_text = f"Explanation:\n\n{response['explanation']}"
                self.explanation['state'] = 'normal'
                self.explanation.delete('1.0', tk.END)
                self.explanation.insert(tk.END, explanations_text)
                self.explanation['state'] = 'disabled'
                self.explanation.tag_add("tag_center", '1.0')
                self.explanation.tag_configure("tag_center", justify='center')

                # Changing button set image wallpaper

                self.wallpaper_btn['command'] = lambda: set_wallpaper(self.name_picture)

                if self.name_picture in recv_image():
                    Images = tk.PhotoImage(file='LOGO APP/button/favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
                else:
                    Images = tk.PhotoImage(file='LOGO APP/button/not favoris.png').subsample(16)
                    self.favoris_btn.photo = Images
                    self.favoris_btn['image'] = Images
            else:
                print(
                    f"/!\ Unfortunately, on this day, NASA to publish {response['media_type']} is not an image! Try tomorrow :)")
                if response['media_type'].lower()[0:5] == 'video':
                    print('\nIf you want to see the video :\n'
                          f"URL : {response['url']}")


def Nasa():
    try:
        request = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={recv_token()}")
        response = request.json()
        
        if response['media_type'].lower()[0:5] == 'image':
            url_picture = response['url']
            ScrapImage(url_picture)
            ScrapColor_Img(url_picture)
        else:
            print(
                f"/!\ Unfortunately, on this day, NASA to publish {response['media_type']} is not an image! Try tomorrow :)")
            if response['media_type'].lower()[0:5] == 'video':
                print('\nIf you want to see the video :\n'
                      f"URL : {response['url']}")
    except KeyError as e:
        print("You need to fill in your api key in the app 'add your token'")


Nasa()
