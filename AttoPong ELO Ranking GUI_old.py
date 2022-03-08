######################################

# ATTOPONG RANKING WITH ELO RATINGS

# by Mauro 01/10/2020

# GUI TO UPDATE CURRENT RANKING

############## IMPORT ################
import math
import ast
import tkinter as tk
import tkinter.ttk as ttk
from shutil import copyfile
from datetime import datetime
import winsound
from PIL import Image, ImageTk


######################################

########## DEFINE FUNCTIONS ##########

# Functions to make sounds
def sound1():
    freq = 420
    winsound.Beep(freq, 300)
    winsound.Beep(freq, 150)
    winsound.Beep(freq, 150)
    winsound.Beep(int(freq * (2) ** (12 / 12)), 900)


def sound2():
    freq = 420
    winsound.Beep(freq, 400)
    winsound.Beep(int(freq * (2) ** (4 / 12)), 150)
    winsound.Beep(int(freq * (2) ** (7 / 12)), 150)
    winsound.Beep(int(freq * (2) ** (12 / 12)), 450)
    winsound.Beep(int(freq * (2) ** (11 / 12)), 150)
    winsound.Beep(int(freq * (2) ** (12 / 12)), 900)


def sound3():
    freq = 420
    winsound.Beep(freq, 500)
    winsound.Beep(int(freq / (2) ** (5 / 12)), 600)


# Function to calculate the Probability
def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


# Function to calculate Elo rating
def EloRating(R1, R2, pt1, pt2):
    K = 40
    kdiff = abs(pt1 - pt2) / 9 + 0.25

    # Calculate the Winning Probability of Players 1 and 2
    P1 = Probability(R2, R1)
    P2 = 1 - P1

    # Case -1 Player A wins
    if (pt1 > pt2):
        R1 = R1 + K * (1 - P1) * kdiff
        R2 = R2 + K * (0 - P2) * kdiff

    # Case -2 Player B wins
    if (pt1 < pt2):
        R1 = R1 + K * (0 - P1) * kdiff
        R2 = R2 + K * (1 - P2) * kdiff

    return [round(R1, 0), round(R2, 0)]


################################################

###### READ RANKING FILE & MAKE COPY ############
file = open("CurrentRanking.txt", "r")  # It should be a file with written: {'Mauro': 1000.0, 'David': 1000.0, ... }
Attopong = ast.literal_eval(file.read())
file.close()
now = datetime.now()
copyfile("CurrentRanking.txt", "Ranking_" + now.strftime("%d%b%Y-%Hh%M") + ".txt")
#################################################

############### GUI #############################

listPlayers = ('David', 'Martin', 'Mauro', 'Mekha', 'Romain', 'Thierry', 'Constant', 'Lucie', 'Hugo')

window = tk.Tk()

window.title("ATTOPONG RANKING")

window.geometry('355x480')

lbl_player = tk.Label(window, text='Player')
lbl_player.grid(column=0, row=2)

comboP1 = ttk.Combobox(window, width=8)  # Select player one
comboP1['values'] = listPlayers
comboP1.grid(column=1, row=2)

comboP2 = ttk.Combobox(window, width=8)  # Select player two
comboP2['values'] = listPlayers
comboP2.grid(column=2, row=2)

lbl_score = tk.Label(window, text='Match score')
lbl_score.grid(column=0, row=3)

entryR1 = tk.Entry(window, width=6)  # Score player one
entryR1.grid(column=1, row=3)
entryR1.focus()

entryR2 = tk.Entry(window, width=6)  # Score player two
entryR2.grid(column=2, row=3)

sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
whiteboard = ' '.join([str(elem) for elem in sortedAttopong])
whiteboard = whiteboard.replace(") (", "\n")
whiteboard = whiteboard.replace("'", "")
whiteboard = whiteboard.replace(",", "  ")
whiteboard = whiteboard.replace("(", "\n  ")
whiteboard = whiteboard.replace(")", "\n")
lbl_Attopong = tk.Label(window, text=whiteboard)  # Display the whiteboard
lbl_Attopong.grid(column=0, row=1, columnspan=4)


def update_ranking():
    makesound = 0
    sortedAttopong_old = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
    P1 = [comboP1.get(), int(entryR1.get())]
    P2 = [comboP2.get(), int(entryR2.get())]
    if P1[0] != P2[0]:
        score = EloRating(Attopong[P1[0]], Attopong[P2[0]], P1[1], P2[1])
        Attopong[P1[0]] = score[0]
        Attopong[P2[0]] = score[1]
        with open('CurrentRanking.txt', 'w') as f:
            print(Attopong, file=f)
        sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(listPlayers)):
            if (sortedAttopong[i][0]) != (sortedAttopong_old[i][0]):
                makesound += 1
        if makesound == 0:
            sound1()
        else:
            sound2()
        whiteboard = ' '.join([str(elem) for elem in sortedAttopong])
        whiteboard = whiteboard.replace(") (", "\n")
        whiteboard = whiteboard.replace("'", "")
        whiteboard = whiteboard.replace(",", "   ")
        whiteboard = whiteboard.replace("(", "  ")
        whiteboard = whiteboard.replace(")", "")
        lbl_Attopong = tk.Label(window, text=whiteboard)
        lbl_Attopong.grid(column=0, row=1, columnspan=4)


btn = tk.Button(window, text="Update", command=update_ranking)
btn.grid(column=3, row=3)


def reloadlast_ranking():
    sound3()
    file_old = open("Ranking_" + now.strftime("%d%b%Y-%Hh%M") + ".txt", "r")
    Attopong = ast.literal_eval(file_old.read())
    file.close()
    with open('CurrentRanking.txt', 'w') as f:
        print(Attopong, file=f)
    sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
    whiteboard = ' '.join([str(elem) for elem in sortedAttopong])
    whiteboard = whiteboard.replace(") (", "\n")
    whiteboard = whiteboard.replace("'", "")
    whiteboard = whiteboard.replace(",", "   ")
    whiteboard = whiteboard.replace("(", "  ")
    whiteboard = whiteboard.replace(")", "")
    lbl_Attopong = tk.Label(window, text=whiteboard)
    lbl_Attopong.grid(column=0, row=1, columnspan=4)


btnreload = tk.Button(window, text="Reload", command=reloadlast_ranking)
btnreload.grid(column=0, row=0, columnspan=4)

image = Image.open("Attopong4.png")
photo = ImageTk.PhotoImage(image)
label_img = tk.Label(image=photo)
label_img.image = photo
label_img.grid(column=0, row=5, columnspan=4)

window.mainloop()
#################################################