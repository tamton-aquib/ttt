#!/usr/bin/env python3
from tkinter import *
import sys
from words import words as list_of_words
import random
import json

# Names and Variables
with open('config.json') as config_file:
    data = json.load(config_file)

max_length_of_a_word = data['max_length_of_a_word']
total_words_to_appear = data['total_words_to_appear']
MainStart = data['time_allowed']

words = []
while len(words) < total_words_to_appear:
    random_word = random.choice(list_of_words)
    if len(random_word) <= max_length_of_a_word:
        words.append(random_word)

start = MainStart
correct_words_count = 0
unused_variable = '#316879, #f47a60, #7fe7dc, #ced7d8'


# ======== STYLING ==========

label_fg = '#000000'
label_bg = '#316878'
entry_fg = '#000000'
entry_bg = '#7fe7dc'

label_configs = {
    "height": "10",
    "font": "Sans 16",
    "bg": label_bg,
    "fg": label_fg,
    "wraplength": "650"
}

entry_configs = {
    "font": "Sans",
    "borderwidth": "3",
    "width": "50",
    "bg": entry_bg,
    "fg": entry_fg
}

timer_label_configs = {
    "font": "Sans 14",
    "bg": label_bg,
    "fg": label_fg
}

score_configs = {
    "bg": label_bg,
    "fg": label_fg,
    "font": "Sans 16"
}

# ========== WIDGETS ==========

# Root widget
root = Tk()
root.geometry("800x500")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (800/2))
y_cordinate = int((screen_height/2) - (500/2))
root.geometry(f"800x500+{x_cordinate}+{y_cordinate}")
root.title("Noice")
root.configure(bg=label_bg)

label = Label(root, text=" ".join(words), **label_configs)
label.pack()

timer_label = Label(root, text=start, **timer_label_configs)
timer_label.pack(pady=2)

entry = Entry(root, **entry_configs)
entry.pack()
entry.focus()


def display_score():
    global correct_words_count
    score = (correct_words_count / int(MainStart)) * 60
    Label(root, text=f"You score is: {score}", **score_configs).pack(pady=20)
    print(f"Your score is: {score}")
    timer_label.config(text="0")

# ========= CLOCK ==========


def timer():
    global start
    if int(start) <= 1:
        print("Timeout")
        display_score()
        return
    start = str(int(start)-1)
    timer_label.config(text=start)
    timer_label.after(1000, timer)


timer()


def main(event):
    global start
    global correct_words_count
    if event.char == " ":
        string = entry.get().strip()
        if string == "x":
            sys.exit()

        if string in words:
            words.remove(string)
            correct_words_count += 1

        entry.delete(0, END)


root.bind('<space>', main)

root.mainloop()
