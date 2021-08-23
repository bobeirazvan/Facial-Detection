#CLAUZE IMPORT
import tkinter as tk
import random
import time
from detect_face_webcam import face_webcam

#FROM HERE MAINLY GUI

window=tk.Tk()
window.title("Face Detection using Haar Cascade")
window.geometry("640x360")

HEIGHT = 600
WIDTH = 500

#CANVAS

background_image=tk.PhotoImage(file='image1.png')
background_label=tk.Label(window, image=background_image)
background_label.place(relwidth=1,relheight=1)

window.resizable(False,False)

#FUNCTIONS
def phrase_generator():
    phrases=["Salut", "Buna","Ceau","Hei",]
    nume=str(name.get())
    global numeaux
    numeaux=str(nume)
    return phrases[random.randint(0,3)]+" "+ nume + " ! "
#functie de iesire
def quit():
    time.sleep(5)
    window.destroy()

def phrase_display():
    greeting=phrase_generator()
    greeting_display = tk.Text(master=window,bg="Cyan4",fg="white", height=15, width=41,)
    greeting_display.grid(column=0, row=3)
    greeting_display.insert(tk.END, greeting)
    window.update()
    quit()

#LABEL
title=tk.Label(text="Cum te numesti?",fg="white",bg="cyan4")
title.grid(column=0,row=0)

#BUTTON
button1=tk.Button(text="Submit", command=phrase_display)
button1.grid(column=0,row=2)
#ENTRY FIELD
name=tk.Entry()
name.grid(column=0, row=1)

#TEXT FIELDS
text_field=tk.Text(master=window,bg="Cyan4", height=15, width=41)
text_field.grid(column=0, row=3)

window.mainloop()
face_webcam(numeaux)
