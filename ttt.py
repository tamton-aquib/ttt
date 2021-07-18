#!/usr/bin/env python3
from tkinter import Tk, Label, Entry, END
import sys, random, json

from words import words as list_of_words
import styling

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

# ========== WIDGETS ==========

# Root widget
root = Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (800/2))
y_cordinate = int((screen_height/2) - (500/2))
root.geometry(f"800x500+{x_cordinate}+{y_cordinate}")
root.title("Typing speed test.")
root.configure(bg=styling.label_bg)

label = Label(root, text=" ".join(words), **styling.label_configs).pack()

timer_label = Label(root, text=start, **styling.timer_label_configs)
timer_label.pack(pady=2)

entry = Entry(root, **styling.entry_configs)
entry.pack()
entry.focus()

def display_score():
    global correct_words_count
    score = (correct_words_count / int(MainStart)) * 60
    Label(root, text=f"You score is: {score} WPM",
          **styling.score_configs).pack(pady=20)
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
