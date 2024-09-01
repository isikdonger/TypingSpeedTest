import os
from tkinter import *
import string
import random
from datetime import datetime
import requests

FONT = ("Arial", 12, "bold")
TEXT_LENGTH = 80


def create_rnd_text():
    # word_dict = requests.get("https://random-word-api.herokuapp.com/all").json()
    # text = ""
    # for i in range(TEXT_LENGTH):
    #     if i == 0:
    #         text += random.choice(word_dict)
    #         text.capitalize()
    #         text += " "
    #     else:
    #         text += random.choice(word_dict)
    #         text += " "
    text_dict = requests.get(f"https://random-word-api.herokuapp.com/word?number={TEXT_LENGTH}").json()
    text_dict[0] = text_dict[0].capitalize()
    print(text_dict)
    text = ""
    for word in text_dict:
        text += word
        text += " "
    return text


def reset():
    global rnd_txt, main_text, wps_label, accuracy_label, start_time
    rnd_txt = create_rnd_text()
    main_text.config(state=NORMAL)
    main_text.delete(1.0, END)
    main_text.insert(END, chars=rnd_txt)
    main_text.config(state=DISABLED)
    wps_label.config(text="WpS: ")
    accuracy_label.config(text="Acc: ")
    start_time = None


def calculate_results(event=None):
    global start_time, user_text, main_text, wps_label, accuracy_label
    if start_time is None:
        return

    end_time = datetime.now()
    time_diff = end_time - start_time
    total_seconds = time_diff.total_seconds()

    user_text_str = user_text.get(1.0, END).strip().strip()
    main_text_str = main_text.get(1.0, END).strip().strip()

    word_count = len(user_text_str.split())
    wps = word_count / total_seconds if total_seconds > 0 else 0
    wps_label.config(text=f"WpS: {wps:.2f}")

    correct_chars = 0
    total_chars = min(len(user_text_str), len(main_text_str))
    for i in range(total_chars):
        if user_text_str[i] == main_text_str[i]:
            correct_chars += 1

    accuracy = (correct_chars / len(main_text_str)) * 100 if main_text_str else 0
    accuracy_label.config(text=f"Acc: {accuracy:.2f}%")


def on_key_press(event):
    global start_time
    if start_time is None:
        start_time = datetime.now()


rnd_txt = create_rnd_text()

window = Tk()
window.title("Typing Speed Tester")
window.config(padx=20, pady=20, width=100, height=150)

wps_label = Label(text="WpS: ")
wps_label.grid(row=0, column=1, padx=5, pady=5)
accuracy_label = Label(text="Acc: ")
accuracy_label.grid(row=0, column=2, padx=5, pady=5)

user_text = Text(height=20, width=50, wrap=WORD, fg="black", font=FONT)
user_text.grid(row=1, column=0)
user_text.bind("<KeyPress>", on_key_press)
user_text.bind("<Return>", calculate_results)

main_text = Text(height=20, width=50, wrap=WORD, fg="black", font=FONT)
main_text.insert(END, chars=rnd_txt)
main_text.config(state=DISABLED)
main_text.grid(row=1, column=3)

reset_btn = Button(width=12, bg="red", fg="white", text="Reset", command=reset, highlightthickness=0)
reset_btn.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

start_time = None

window.mainloop()
