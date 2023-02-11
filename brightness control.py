import pystray, threading
import screen_brightness_control as sbc
from pystray import MenuItem as item
from PIL import Image,ImageDraw
from tkinter import ttk
import tkinter as tk

# создание иконки для трея
image = Image.new(mode="RGBA", size=(256, 256))
draw = ImageDraw.Draw(image, 'RGBA')
d = 128
R = 60
r = 40
draw.ellipse((d - R, d - R, d + R, d + R), fill=(255, 255, 255, 255))
draw.ellipse((d - r, d - r, d + r, d + r), fill=(255, 255, 255, 0))
width = 24
r_start = 80
draw.line(((r_start + d, 0 + d), (128 + d, 0 + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((-r_start + d, 0 + d), (-128 + d, 0 + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((0 + d, r_start + d), (0 + d, 128 + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((0 + d, -r_start + d), (0 + d, -128 + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((int(r_start * 0.7) + d, int(r_start * 0.7) + d), (int(128 * 0.7) + d, int(128 * 0.7) + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((int(-r_start * 0.7) + d, int(-r_start * 0.7) + d), (int(-128 * 0.7) + d, int(-128 * 0.7) + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((int(-r_start * 0.7) + d, int(r_start * 0.7) + d), (int(-128 * 0.7) + d, int(128 * 0.7) + d)), fill=(255, 255, 255, 255), width=width)
draw.line(((int(r_start * 0.7) + d, int(-r_start * 0.7) + d), (int(128 * 0.7) + d, int(-128 * 0.7) + d)), fill=(255, 255, 255, 255), width=width)
del draw


root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry('300x80+1400+960')
root.overrideredirect(True)

canvas = tk.Canvas(root, width=300, height=80, highlightthickness=2, highlightbackground="#adadad")
canvas.pack()


def quit_window(icon, item):
    icon.stop()
    root.destroy()


def show_window(icon, item):
    global is_show
    icon.stop()
    root.after(0, root.deiconify)
    root.after(1, lambda: root.focus_force())
    root.after(1, lambda: root.bind('<FocusOut>', minimize_window))
    is_show = True


def minimize_window(*args):
    global is_show
    if is_show:
        is_show = False
        root.unbind('<FocusOut>')
        root.withdraw()
        menu = pystray.Menu(item('Quit', quit_window), item('Show', show_window, default=True))
        icon = pystray.Icon("name", image, "brightness", menu)
        icon.run()


def brightness_updates_listener():
    global cur_brightness, scale_brightness

    if scale_brightness != cur_brightness and threading.active_count() == 1:
        cur_brightness = scale_brightness
        th = threading.Thread(target=sbc.set_brightness, args=(cur_brightness,))
        th.start()

    elif sbc.get_brightness() != cur_brightness and threading.active_count() == 1:
        cur_brightness = sbc.get_brightness()
        scale.set(cur_brightness)
        text_label.configure(text=str(cur_brightness))

    root.update()
    root.update_idletasks()
    root.after(250, brightness_updates_listener)


def set_scale_brightness(val):
    global scale_brightness
    scale_brightness = int(str(val).split('.')[0])
    text_label.configure(text=str(scale_brightness))


is_show = True
cur_brightness = sbc.get_brightness()

text_label = tk.Label(canvas, text=str(cur_brightness), font=(None, 14))
text_label.place(x=38, y=38, anchor="center")

# ползунок яркости
scale_brightness = cur_brightness
scale = ttk.Scale(canvas, from_=0, to=100, length=200, orient="horizontal", command=set_scale_brightness)
scale.set(cur_brightness)
scale.place(x=75, y=25)

brightness_updates_listener()

minimize_window()

root.mainloop()
