
# Project realized by Maxence R.
# Fan of Space !
# Love Nasa

# Import Module

import shutil
import tkinter
import requests
from PIL.Image import *
from pathlib import Path
import wget
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from requests import get
import pytube


def youtube_download_video(link):
    youTube = pytube.YouTube(link)
    stream = youTube.streams.get_highest_resolution()
    stream.download()


def ScrapImage(url: str = None) -> None:
    i = wget.detect_filename(url)
    path = Path(f'.\image\{i}')
    if path.exists():
        os.remove(f'.\image\{i}')

    wget.download(url, 'image')


def ScrapColor_Img(url: str = None) -> None:
    i = wget.detect_filename(url)

    image = open(f'.\image\{i}')
    x = 10
    y = 30
    (red, green, blue) = image.getpixel((x, y))
    Interface(red, green, blue, i)


def _rgb(rgb):
    return "#%02x%02x%02x" % rgb


def set_wallpaper(img):
    images = img
    path_os = os.getcwd()
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{path_os}\image\{images}", 0)
    print('The wallpaper was well changed !')


def Interface(r: str = None, g: str = None, b: str = None, name_picture: str = None) -> None:
    request = get(
        'https://api.nasa.gov/planetary/apod?api_key=oQhM7q2xBtR10u4pjawCmF4HKGtc8a7ewS9mL6W6')
    data = request.json()

    windows = tk.Tk()

    path_img = f'./image/{name_picture}'

    windows.config(background=_rgb((r, g, b)))
    windows.geometry('1080x720')
    windows.title(f'{name_picture} | Informations | One Day, One Image ! NASA')
    windows.iconbitmap('./LOGO APP/logo.ico')

    img = Image.open(path_img)
    Images = img.resize((558, 720), Image.ANTIALIAS)
    Images = ImageTk.PhotoImage(Images)
    Picture = tk.Label(windows, image=Images, bd=0, bg='white')
    Picture.pack(side=tk.LEFT)

    Title = tk.Label(windows, text=f"\n{data['title']}", bg=_rgb((r, g, b)), fg='white', font=('Arial', 16, 'bold'))
    Title.pack()

    Author = tk.Label(windows, text=f"\nAuthor: {data['copyright']}", bg=_rgb((r, g, b)), fg='white',
                      font=('Arial', 11))
    Author.pack()

    Date_picture = tk.Label(windows, text=f"Date of picture: {data['date']}", bg=_rgb((r, g, b)), fg='white',
                            font=('Arial', 11))
    Date_picture.pack()

    Explanation_text = f"Explanation:\n\n{data['explanation']}"

    Explanation = tkinter.Text(windows, height=18)
    Explanation.insert(tk.END, Explanation_text)
    Explanation.config(state='disabled', bg=_rgb((r, g, b)), fg='white', font=('Arial', 11), bd=0)
    Explanation.tag_add("tag_center", '1.0')
    Explanation.tag_configure("tag_center", justify='center')

    Explanation.pack()

    wallpaper_btn = tk.Button(windows, text="Set like Wallpaper", bd=0,
                              bg=_rgb((int(r) + 20, int(g) + 20, int(b) + 20)), fg='white', font=('Arial', 11, 'bold'),
                              activebackground=_rgb((int(r) + 20, int(g) + 20, int(b) + 20)), activeforeground='white',
                              command=lambda: set_wallpaper(name_picture))
    wallpaper_btn.pack(ipadx=20, ipady=20, pady=50)

    windows.mainloop()


def Nasa():
    request = requests.get("https://api.nasa.gov/planetary/apod?api_key=oQhM7q2xBtR10u4pjawCmF4HKGtc8a7ewS9mL6W6")
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

            domain = 'youtube.com'

            if domain in response['url']:
                youtube_download_video(response['url'])
                path_file = os.getcwd()
                # Source path
                source = f"{path_file}/{response['title']}.mp4"

                # Destination path
                destination = f"{path_file}/video"
                shutil.move(source, destination)
                print("\nThe video was downloadable!")
            else:
                print("\nI'm sorry, I tried, but I can't download the video!")


Nasa()
