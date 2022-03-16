######################################

# ATTOPONG RANKING WITH ELO RATINGS

# by Mauro 01/10/2020

# GUI TO UPDATE CURRENT RANKING

############## IMPORT ################
import ast
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from shutil import copyfile
from datetime import datetime
import winsound
from PIL import Image, ImageTk
from tkinter import HORIZONTAL, Variable, messagebox
import matplotlib.pyplot as plt
import pandas as pd
import os
from idlelib.tooltip import Hovertip

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
    return 1. / (1. + (10**( (rating1 - rating2) / 400) ))

def GetScaling(formula,point_diff,ranking_diff):
    if formula:
        K = 40
        kdiff = point_diff / 9 + 0.25
    else:
        K = 50
        alpha = 1.5
        kdiff = np.log( 1. + point_diff ) * (alpha / (alpha - ranking_diff / 1000))
    return K*kdiff
# Function to calculate Elo rating 
def EloRating(R1, R2, pt1, pt2, formula = 0):    
    #Get scaling (rate of change as a function of elo and point difference)
    scaling_coeff = GetScaling(formula,abs(pt1-pt2),R2-R1)        
    # Calculate the Winning Probability of Players 1 and 2
    P1 = Probability(R2, R1) #Probability for player 2 to win versus player 1        
    #If player 1 wins ==) int(pt1>pt2) = 1 ==) (int(pt1>pt2) - P1) = P2
    #If player 2 wins ==) int(pt1>pt2) = 0 ==) (int(pt1>pt2) - P1) = -P1
    elo_modification = round(scaling_coeff * (int(pt1>pt2) - P1), 0) #Change in elo for both players      
    #Update ranking
    return elo_modification


################################################
def updateWhiteboard(window,sortedAttopong):
    whiteboard = ' '.join([str(elem) for elem in sortedAttopong])
    whiteboard = whiteboard.replace(") (", "\n")
    whiteboard = whiteboard.replace("'", "")
    whiteboard = whiteboard.replace(",", "   ")
    whiteboard = whiteboard.replace("(", "  ")
    whiteboard = whiteboard.replace(")", "")
    lbl_Attopong = tk.Label(window, text=whiteboard)
    lbl_Attopong.grid(column=0, row=1, columnspan=4)
###### READ RANKING FILE & MAKE COPY ############
file = open("CurrentRanking.txt", "r")  # It should be a file with written: {'Mauro': 1000.0, 'David': 1000.0, ... }
datafile = file.read().splitlines()
Attopong = ast.literal_eval(datafile[-1])  # Take last line (latest) for display
if 'Time' in Attopong:
    del Attopong['Time']  # Remove timestamp
file.close()

#################################################

############### GUI #############################

listPlayers = ('David', 'Martin', 'Mauro', 'Mekha', 'Romain', 'Thierry', 'Constant', 'Lucie', 'Hugo')

window = tk.Tk()

window.title("ATTOPONG RANKING")

window.geometry('355x520')


n = 2
#DATE
lbl_date = tk.Label(window, text='Match Date')
lbl_date.grid(column=0, row=n)
entry_text=tk.StringVar()
entry_date = tk.Entry(window, width=10,textvariable= entry_text)  # Score player one
entry_date.grid(column=1, row=n, columnspan=2)
entry_text.set(datetime.now().strftime("%Y%m%d"))
myTip = Hovertip(entry_date,'Format is YearMonthDate (20220309)')

n+=1
#PLAYER
lbl_player = tk.Label(window, text='Player')
lbl_player.grid(column=0, row=n)

comboP1 = ttk.Combobox(window, width=8)  # Select player one
comboP1['values'] = listPlayers
comboP1.grid(column=1, row=n)

comboP2 = ttk.Combobox(window, width=8)  # Select player two
comboP2['values'] = listPlayers
comboP2.grid(column=2, row=n)

n+=1
#SCORE
lbl_score = tk.Label(window, text='Match score')
lbl_score.grid(column=0, row=n)

entryR1 = tk.Entry(window, width=6)  # Score player one
entryR1.grid(column=1, row=n)
entryR1.focus()

entryR2 = tk.Entry(window, width=6)  # Score player two
entryR2.grid(column=2, row=n)

sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
# Update whiteboard display
updateWhiteboard(window,sortedAttopong)



def update_ranking():
    ###### READ RANKING FILE & MAKE COPY ############
    file = open("CurrentRanking.txt", "r")  # It should be a file with written: {'Mauro': 1000.0, 'David': 1000.0, ... }
    datafile = file.read().splitlines()
    Attopong = ast.literal_eval(datafile[-1])  # Take last line (latest) for display
    if 'Time' in Attopong:
        del Attopong['Time']  # Remove timestamp
    file.close()    
    makesound = 0
    sortedAttopong_old = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
    P1 = [comboP1.get(), int(entryR1.get())]
    P2 = [comboP2.get(), int(entryR2.get())]
    if P1[0] != P2[0]:
        #Find change in elo
        elo_modification = EloRating(Attopong[P1[0]], Attopong[P2[0]], P1[1], P2[1],formula = 0) #Index of formula now picks the elocoeff chosen
        # Update ranking
        Attopong[P1[0]] +=  elo_modification
        Attopong[P2[0]] -=  elo_modification
        # Time stamp to add to the save file
        try:
            match_date = datetime.strptime(str(entry_date.get()), "%Y%m%d").strftime("%d/%m/%Y") #Get date
        except:           
            match_date = datetime.now().strftime("%d/%m/%Y") #Get current date if error

        timestamp = {'Time': match_date}
        #File that keeps track of all matches
        df =pd.DataFrame({'Date': [ match_date],
                        'Player1': [P1[0]],
                        'Player2': [P2[0]],
                        'Score1': [P1[1]],
                        'Score2': [P2[1]]})
        df.to_csv('ScoreSheet\\2022.txt', mode='a', index=False,header=not os.path.exists('ScoreSheet\\2022.txt'),sep='\t')
        #Update results
        with open('CurrentRanking.txt', 'a') as f:
            f.write(str({**timestamp, **Attopong}) + '\n')

        # Make sounds
        sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(listPlayers)):
            if (sortedAttopong[i][0]) != (sortedAttopong_old[i][0]):
                makesound += 1
        if makesound == 0:
            sound1()
        else:
            sound2()

        # Update whiteboard display
        updateWhiteboard(window,sortedAttopong)

        # Pop up window showing evolution
        if elo_modification > 0:
            messagebox.showinfo('Rankings Updated!',
                                P1[0] + ' took ' + str(elo_modification) + ' points from ' + P2[
                                    0] + '!')
        else:
            messagebox.showinfo('Rankings Updated!',
                                P2[0] + ' took ' + str(abs(elo_modification)) + ' points from ' + P1[
                                    0] + '!' )


btn = tk.Button(window, text="Update", command=update_ranking)
btn.grid(column=3, row=3)

def plot_history():
    plt.figure(num='Attopong Ranking History')

    # This assumes that all players are in every line
    with open("CurrentRanking.txt", "r") as f: # It should be a file with written: {'Mauro': 1000.0, 'David': 1000.0, ... }
        datafile = f.read().splitlines() #Extract each line from file            
    timestamps = []
    ranking_history = {}
    data_dict = [ast.literal_eval(l) for l in datafile]

    for entry in data_dict[0]:
        if entry == 'Time':
            timestamps = [d['Time'] for d in data_dict]
        else:
            ranking_history[entry] = [d[entry] for d in data_dict]

    for player in ranking_history:
        plt.plot(np.asarray(ranking_history[player]), label=str(player))

    plt.legend()
    plt.show()


def reloadlast_ranking():
    sound3()    
    with open("ScoreSheet\\2022.txt", "r") as f: # Open Scoresheet (read)
        datafile = f.read().splitlines() #Extract each line from file        
    with open("ScoreSheet\\2022.txt", "w") as f: # Open Scoresheet (write)
        print("\n".join(datafile[:-1]), file=f) #Rewrite file without last entry
    with open("CurrentRanking.txt", "r") as f: # Open CurrentRanking (read)
        datafile = f.read().splitlines() #Extract each line from file
        Attopong = ast.literal_eval(datafile[-2])  # Take second last line (latest) for display
    with open('CurrentRanking.txt', 'w') as f: # Open CurrentRanking (write)
        print("\n".join(datafile[:-1]), file=f) #Rewrite file without last entry
    if 'Time' in Attopong:
        del Attopong['Time']  # Remove timestamp
    sortedAttopong = sorted(Attopong.items(), key=lambda x: x[1], reverse=True)
    # Update whiteboard display
    updateWhiteboard(window,sortedAttopong)

def reset_ranking():    
    with open("CurrentRanking.txt", "r") as file: # It should be a file with written: {'Mauro': 1000.0, 'David': 1000.0, ... }
        datafile = file.read().splitlines() #Extract each line from file
    Attopong = ast.literal_eval(datafile[0])  # Take first line (latest) for start date    
    try:
        start_date = datetime.strptime(Attopong['Time'],"%d/%m/%Y")
    except:
        start_date = datetime.strptime(Attopong['Time'],"%d%b%Y-%Hh%Mm%Ss")        
    reset_date = datetime.now()
    file_copy = os.path.join(f'ScoreSheet', "Ranking_" + start_date.strftime("%d%m%Y") + '-' + reset_date.strftime("%d%m%Y") + ".txt")
    copyfile("CurrentRanking.txt",file_copy)
    listPlayers = ('David', 'Martin', 'Mauro', 'Mekha', 'Romain', 'Thierry', 'Constant', 'Lucie', 'Hugo')
    dic_time = dict.fromkeys(('Time',), reset_date.strftime('%d/%m/%Y'))
    dic_player = dict.fromkeys(listPlayers, 1000)
    dic_tot = {**dic_time, **dic_player}
    with open('CurrentRanking.txt', 'w') as f:
        print(dic_tot, file=f) #Rewrite file without last entry
    sortedAttopong = sorted(dic_player.items(), key=lambda x: x[1], reverse=True)
    # Update whiteboard display
    updateWhiteboard(window,sortedAttopong)
            

btn = tk.Button(window, text="Reset ranking", command=reset_ranking)
btn.grid(column=2, row=0, columnspan=2)

btn = tk.Button(window, text="Plot history", command=plot_history)
btn.grid(column=1, row=0, columnspan=2)

btnreload = tk.Button(window, text="Reload", command=reloadlast_ranking)
btnreload.grid(column=0, row=0, columnspan=2)

image = Image.open("Attopong4.png")
photo = ImageTk.PhotoImage(image)
label_img = tk.Label(image=photo)
label_img.image = photo
label_img.grid(column=0, row=5, columnspan=4)

window.mainloop()
#################################################
