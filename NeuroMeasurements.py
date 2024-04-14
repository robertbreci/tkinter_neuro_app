import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from random import randint
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def create_page(root, question_label, measurements, navigate_to_page, next_page_num, measurement_range, image_path):
    for widget in root.winfo_children():
        widget.destroy()

    # Image setup
    img = Image.open(image_path)
    img = img.resize((290,245), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    
    img_label = ttk.Label(root, image=photo)
    img_label.image = photo  # keep a reference!
    img_label.pack(pady=5)

    # Setup for other components as before
    question = randint(*measurement_range)
    answers = {label: round(question * percentage / 100, 2) for label, percentage in measurements.items()}

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text=f"If the measurement for {question_label} is: {question}cm\nProvide the following percentages:", font=('Helvetica', 12)).pack(pady=10)

    entry_widgets = {}
    for label_text in answers.keys():
        row = ttk.Frame(frame)
        row.pack(fill='x', pady=3)
        ttk.Label(row, text=label_text, width=30).pack(side='left')
        entry = ttk.Entry(row, width=20, bootstyle='info')
        entry.pack(side='left')
        entry_widgets[label_text] = entry

    result_msg = ttk.Label(frame, text="", font=('Helvetica', 12))
    result_msg.pack(pady=10)

    def check_answers():
        correct = True
        for label_text, correct_answer in answers.items():
            try:
                user_answer = float(entry_widgets[label_text].get())
                if user_answer == correct_answer:
                    entry_widgets[label_text].configure(bootstyle='success')
                else:
                    entry_widgets[label_text].configure(bootstyle='danger')
                    correct = False
            except ValueError:
                entry_widgets[label_text].configure(bootstyle='warning')
                correct = False
        result_msg['text'] = "All answers correct!" if correct else "Please check your answers, some are incorrect."

    ttk.Button(frame, text="Check answers", command=check_answers, bootstyle='primary').pack(pady=10)
    ttk.Button(frame, text=f"Go to Page {next_page_num}", command=lambda: navigate_to_page(next_page_num), bootstyle='secondary').pack(pady=10)

def create_start_page(root, navigate_to_page):
    # Clear previous content
    for widget in root.winfo_children():
        widget.destroy()
    start_image_path = resource_path(r'assets\images\animated.gif')
    start_img = Image.open(start_image_path)
    start_img = start_img.resize((290,245), Image.LANCZOS)
    start_photo = ImageTk.PhotoImage(start_img)
    
    img_label = ttk.Label(root, image=start_photo)
    img_label.image = start_photo  # keep a reference!
    img_label.pack(pady=5)
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text="Neuro Measurement Practice App", font=('Helvetica', 16)).pack(pady=10)
    ttk.Label(frame, text="A randomized measurement will be provided,\nFill in answers and click Check Answers button", font=('Helvetica', 12)).pack(pady=10)
    ttk.Button(frame, text="Start Quiz", command=lambda: navigate_to_page(1), bootstyle='success').pack(pady=20)
def main():
    app = ttkb.Window(themename="pulse")
    app.title("Neuro Measurement Practice App")
    app.geometry('400x950')

    def navigate_to_page(page_number):
        page_settings = {
            1: ("nasion to inion", {
                    "Nasion to FPz (10%)": 10,
                    "Nasion to Fz (30%)": 30,
                    "Nasion to Cz (50%)": 50,
                    "Nasion to Pz (70%)": 70,
                    "Nasion to Oz (90%)": 90
                }, (20, 40), 2,'assets/images/page1.png'),
            2: ("L pre-auricular to R pre-aricular", {
                    "L pre to T3 (10%)": 10,
                    "L pre to C3 (30%)": 30,
                    "L pre to C2 (50%)": 50,
                    "L pre to C4 (70%)": 70,
                    "L pre to T4 (90%)": 90
                }, (10, 30), 3,'assets/images/page2.png'),
            3: ("circumference", {
                    "Fpz to Fp2 (5%)": 5,
                    "Fpz to F8 (15%)": 15,
                    "Fpz to T4 (25%)": 25,
                    "Fpz to T6 (35%)": 35,
                    "Fpz to O2 (45%)": 45,
                    "Fpz to FP1 (5%)": 5,
                    "Fpz to F7 (15%)": 15,
                    "Fpz to T3 (25%)": 25,
                    "Fpz to T5 (35%)": 35,
                    "Fpz to O1 (45%)": 45,
                    "O1 to O2 (10%)": 10,
                    "FP1 to Fp2 (10%)": 10
                }, (30, 62), 4,'assets/images/page3.png'),
            4: ("F7 to F8", {
                    "F7 to F3 (25%)": 25,
                    "F7 to Fz (50%)": 50,
                    "F7 to F4 (75%)": 75
                }, (10, 30), 5,'assets/images/page4.png'),
            5: ("T5 to T6", {
                    "T5 to P3 (25%)": 25,
                    "T5 to Pz (50%)": 50,
                    "T5 to P4 (75%)": 75
                }, (10, 30), 6,'assets/images/page5.png'),
            6: ("Fp1 to O1", {
                    "Fp1 to F3 (25%)": 25,
                    "Fp1 to C3 (50%)": 50,
                    "Fp1 to P3 (75%)": 75
                }, (10, 35), 7,'assets/images/page6.png'),
            7: ("FP2 to O2", {
                    "Fp2 to F4 (25%)": 25,
                    "Fp2 to C4 (50%)": 50,
                    "Fp2 to P4 (75%)": 75
                }, (10, 35), 0,'assets/images/page7.png')
        }
        if page_number == 0:
            create_start_page(app, navigate_to_page)
        else:
            label, measures, range_, next_page, image_path = page_settings[page_number]
            create_page(app, label, measures, navigate_to_page, next_page, range_, image_path)

    navigate_to_page(0)
    app.mainloop()

if __name__ == "__main__":
    main()
