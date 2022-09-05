#!/usr/bin/env python3
from tkinter import Tk, Label, Entry, END
import sys, random, json
from dataclasses import dataclass

import styling

with open('config.json') as config_file:
    data = json.load(config_file)

max_length_of_a_word = data['max_length_of_a_word']
total_words_to_appear = data['total_words_to_appear']
time_allowed = data['time_allowed']

@dataclass
class Ttt:
    root = Tk()
    correct_words_count = 0
    start = time_allowed

    def __init__(self) -> None:
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (800/2))
        y_cordinate = int((screen_height/2) - (500/2))
        self.root.geometry(f"800x500+{x_cordinate}+{y_cordinate}")
        self.root.title("Typing speed test.")
        self.root.configure(bg=styling.label_bg)

        self.words = self.get_random_words()
        Label(self.root, text=" ".join(self.words), **styling.label_configs).pack()

        self.timer_label = Label(self.root, text=self.start, **styling.timer_label_configs)
        self.timer_label.pack(pady=2)

        self.entry = Entry(self.root, **styling.entry_configs)
        self.entry.pack()
        self.entry.focus()

    def get_random_words(self):
        with open('words.txt') as f:
            list_of_words = f.read().split()

        return random.sample(list_of_words, k=total_words_to_appear)

    def display_score(self):
        score = (self.correct_words_count / int(time_allowed)) * 60
        Label(self.root, text=f"You score is: {score} WPM", **styling.score_configs).pack(pady=20)
        print(f"Your score is: {score}")
        self.timer_label.config(text="0")

    def start_timer(self):
        if int(self.start) <= 1:
            print("Timeout")
            self.display_score()
            return

        self.start = int(self.start)-1
        self.timer_label.config(text=str(self.start))
        self.timer_label.after(1000, self.start_timer)

    def main(self, event):
        if event.char == " ":
            string = self.entry.get().strip()
            if string == "x":
                sys.exit()

            if string in self.words:
                self.words.remove(string)
                self.correct_words_count += 1

            self.entry.delete(0, END)

if __name__ == "__main__":
    app = Ttt()
    app.start_timer()
    app.root.bind('<space>', app.main)
    app.root.mainloop()
