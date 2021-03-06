#!/usr/bin/env python3
from tkinter import *
import sys
from words import words
import random
import time
import json

with open('config.json') as f:
    words_total = json.load(f)['number_of_words']

word = []
while len(word) < words_total:
    random_word = random.choice(words)
    if len(random_word) < 7:
        word.append(random_word)

timer = time.perf_counter()
counter = 0

label_bg = '#aed6dc'
label_fg = '#000000'
entry_bg = '#ff9a8d'
entry_fg = '#000000'
frame_color = label_bg

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (800/2))
y_cordinate = int((screen_height/2) - (500/2))
root.geometry(f"800x500+{x_cordinate}+{y_cordinate}")
root.title("Typing speed")

screen_width = root.winfo_screenwidth() * 0.1

frame = Frame(root,
              height=700,
              width=500,
              bg=frame_color,
              highlightcolor='red'
              )
frame.pack()

label = Label(frame,
              text=" ".join(word),
              height=10,
              width=100,
              bg=label_bg,
              fg=label_fg,
              font="Sans 13",
              wraplength=300,
              justify="center",
              anchor='center'
              )
label.pack(padx=screen_width)


def display_score(total_time):
    score = (counter / total_time) * 60
    label.config(text="Game Over!", anchor="center")
    score = round(score)
    result = "Average" if score > 30 else "Below Average"
    Label(root,
          text=f"Your score is: {score}\n   {result}",
          height=10,
          width=60,
          bg='red' if score < 30 else 'green',
          font="Sans 14"
          ).pack(pady=10)


def check_text(string):
    global total_time
    global counter
    if string == 'exit':
        root.destroy()
        sys.exit()
    if string in word:
        status_label.config(text="✓", font="Sans 20", fg='green')
        word.remove(string)
        t1 = time.perf_counter()
        total_time = t1 - timer
        label.config(text=" ".join(word))
    else:
        counter -= 1
        status_label.config(text="✘", font="Sans 20", fg='red')

    if len(word) == 0 or counter == words_total:
        print("Game over")
        display_score(total_time)


def noice(event):
    global timer
    global total_time
    global counter
    if event.char == " ":
        counter += 1
        string = entry.get().strip()
        check_text(string)
        entry.delete(0, END)


entry = Entry(frame,
              font="Sans",
              borderwidth=3,
              width=50,
              bg=entry_bg,
              fg=entry_fg
              )
entry.pack(padx=10, pady=10)
entry.focus()

status_label = Label(frame, text="Status goes here.", bg=label_bg, fg=label_fg)
status_label.pack()

root.bind('<Key>', noice)

root.mainloop()
