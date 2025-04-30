import tkinter as tk
import pygame
import cv2
import sys
import time
from Same_face_model import check_similarity
from sql_writer import find_data,vote_candidate,mark_voted
from expo import voting_machine

Voter_ID = None
label_Invalid_id = None
root = None

def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_Voter_ID(event):
    global Voter_ID
    global root
    ID = Voter_ID.get()
    img = find_data(ID)
    global label_Invalid_id
    if img == -1:
        label_Invalid_id.place(relx=0.5,rely=0.9,anchor=tk.CENTER)
        return -1
    elif img == -2:
        print("Voted")
        tk._default_root.destroy()
        play_alarm()

    else:
        label_Invalid_id.place_forget()
        live_image_checker(img)
        
def live_image_checker(img,do=-1,indx = -1):
    global Voter_ID
    capture = cv2.VideoCapture(0)
    time.sleep(2)
    _,frame = capture.read()
    capture.release()
    score = check_similarity(img,frame)
    print(score)
    if score > 50:
        if(do == -1):
            indx = voting_machine()
            live_image_checker(img,2,indx)
        if(do == 2):
            print(indx)
            vote_candidate(indx)
            mark_voted(Voter_ID.get())
            Voter_ID.delete(0, tk.END)
    else:
        print("different person")
        tk._default_root.destroy()
        play_alarm()
        sys.exit()
    global root
    root = None

def setup_modern_ui(root):
    from tkinter import Canvas
    from PIL import Image, ImageTk
    canvas = Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    bg_img = Image.open("flag.jpg")
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    bg_img = bg_img.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    bg_tk = ImageTk.PhotoImage(bg_img)
    canvas.create_image(0, 0, anchor="nw", image=bg_tk)
    canvas.bg_img = bg_tk
    canvas.create_rectangle(0, 0, screen_w, screen_h, fill="#000000", stipple="gray50")
    canvas.create_text(screen_w / 2, screen_h * 0.08, text="ST. JOSEPH'S INSTITUTE OF TECHNOLOGY",
                       font=("Segoe UI", int(screen_h * 0.04), "bold"), fill="white")
    canvas.create_text(screen_w / 2, screen_h * 0.14, text="SMART VOTING SYSTEM!",
                       font=("Segoe UI", int(screen_h * 0.04), "bold"), fill="#00ffc8")
    return canvas

def main():
    global root, Voter_ID, label_Invalid_id
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    canvas = setup_modern_ui(root)
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    form_frame = tk.Frame(root, bg="#111111", width=600, height=300)
    form_frame.place(relx=0.5, rely=0.5, anchor='center')
    form_frame.pack_propagate(False)
    label_ID = tk.Label(form_frame, text="Enter Your Voter-ID", font=("Segoe UI", 28, "bold"),
                        fg="white", bg="#111111")
    label_ID.pack(pady=(30, 20))  
    Voter_ID = tk.Entry(form_frame, font=("Segoe UI", 24), width=25, justify='center',
                        bg="#222222", fg="white", insertbackground="white",
                        bd=0, relief='flat', highlightthickness=1, highlightbackground="#00ffc8")
    Voter_ID.pack(pady=(0, 30))
    button = tk.Button(form_frame, text="Continue", font=("Segoe UI", 18, "bold"),
                    bg="#00ffc8", fg="#111111", activebackground="#00e6b0",
                    bd=0, relief='flat', padx=20, pady=10)
    button.bind("<Button-1>", get_Voter_ID)
    button.pack()
    label_Invalid_id = tk.Label(form_frame, text="Invalid Voter ID", font=("Segoe UI", 18),
                                fg="red", bg="#111111")
    root.mainloop()
if __name__ == '__main__':
    main()