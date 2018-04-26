import winsound
import time
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

NOTES = {'B6': 1975.53, 'Ab6': 1661.22, 'B1': 61.74, 'D#0': 19.45, 'D1': 36.71, 'C#5': 554.37, 'A#0': 29.14, 'C3': 130.81, 'C#6': 1108.73, 'F#6': 1479.98, 'E1': 41.2, 'G6': 1567.98, 'G3': 196.0, 'Ab3': 207.65, 'Eb6': 1244.51, 'Db1': 34.65, 'D#2': 77.78, 'F#5': 739.99, 'Db2': 69.3, 'G#3': 207.65, 'B4': 493.88, 'Ab0': 25.96, 'C4': 261.63, 'Gb5': 739.99, 'Gb3': 185.0, 'D#8': 4978.03, 'A2': 110.0, 'F#2': 92.5, 'B7': 3951.07, 'G2': 98.0, 'C#0': 17.32, 'G0': 24.5, 'C1': 32.7, 'F7': 2793.83, 'C2': 65.41, 'A0': 27.5, 'F#1': 46.25, 'E0': 20.6, 'B5': 987.77, 'F1': 43.65, 'A5': 880.0, 'Bb1': 58.27, 'F#7': 2959.96, 'A#3': 233.08, 'G7': 3135.96, 'D7': 2349.32, 'A6': 1760.0, 'Bb2': 116.54, 'B0': 30.87, 'Gb4': 369.99, 'Eb4': 311.13, 'C6': 1046.5, 'F2': 87.31, 'G#6': 1661.22, 'Db6': 1108.73, 'Gb0': 23.12, 'Bb6': 1864.66, 'Gb7': 2959.96, 'G#1': 51.91, 'A1': 55.0, 'E6': 1318.51, 'Bb5': 932.33, 'Bb7': 3729.31, 'F#0': 23.12, 'C#2': 69.3, 'F3': 174.61, 'Eb3': 155.56, 'B3': 246.94, 'Bb0': 29.14, 'A3': 220.0, 'Db8': 4434.92, 'G#7': 3322.44, 'E5': 659.26, 'Ab5': 830.61, 'A#1': 58.27, 'C0': 16.35, 'C8': 4186.01, 'E7': 2637.02, 'C#8': 4434.92, 'Gb2': 92.5, 'C7': 2093.0, 'D#5': 622.25, 'Db5': 554.37, 'Eb7': 2489.02, 'F#4': 369.99, 'C#7': 2217.46, 'D6': 1174.66, 'Db4': 277.18, 'D3': 146.83, 'F#3': 185.0, 'D4': 293.66, 'Db7': 2217.46, 'E2': 82.41, 'G4': 392.0, 'D0': 18.35, 'D#1': 38.89, 'Eb0': 19.45, 'F6': 1396.91, 'C#3': 138.59, 'F5': 698.46, 'D#4': 311.13, 'C#4': 277.18, 'D2': 73.42, 'Db0': 17.32, 'Gb6': 1479.98, 'Db3': 138.59, 'D#6': 1244.51, 'A#5': 932.33, 'Ab1': 51.91, 'Eb8': 4978.03, 'Eb1': 38.89, 'Eb5': 622.25, 'C5': 523.25, 'E3': 164.81, 'A#7': 3729.31, 'G1': 49.0, 'Eb2': 77.78, 'A#6': 1864.66, 'A4': 440.0, 'Ab4': 415.3, 'C#1': 34.65, 'Ab2': 103.83, 'G#0': 25.96, 'Gb1': 46.25, 'E4': 329.63, 'D#7': 2489.02, 'A#4': 466.16, 'D5': 587.33, 'D#3': 155.56, 'Bb3': 233.08, 'B2': 123.47, 'A7': 3520.0, 'G5': 783.99, 'F4': 349.23, 'Ab7': 3322.44, 'A#2': 116.54, 'Bb4': 466.16, 'G#5': 830.61, 'G#2': 103.83, 'D8': 4698.64, 'F0': 21.83, 'G#4': 415.3}

def getNote(note):
    """Convert a note into a frequency."""
    found = NOTES.get(note, False)
    if found == False:
        return False
    else:
        return int(found)

def playNote(note, length=250):
    """Convert a note into a frequency, then play it."""
    found = getNote(note.upper())
    if found == False:
        return False
    else:
        winsound.Beep(found, length)

def readPyMus(file):
    """Read data out of a PyMus file."""
    f = open(file, "r")
    name = f.readline().replace("NAME=","").replace("\n","")
    beatlength = int(f.readline().replace("BEATLENGTH=","").replace("\n",""))
    f.readline()
    readlines = f.readlines()
    lines = []
    for i in range(0, len(readlines)):
        lines.append(readlines[i].replace("\n","").split(" "))
    return [name, beatlength, lines]

def parsePyMus(text):
    """Read data from a PyMus string."""
    textlines = text.split("\n")
    name = textlines[0].replace("NAME=","").replace("\n","")
    beatlength = int(textlines[1].replace("BEATLENGTH=","").replace("\n",""))
    lines = []
    readlines = textlines[2:]
    for i in range(0, len(readlines)):
        lines.append(readlines[i].replace("\n","").split(" "))
    return [name, beatlength, lines]

def parseJSON(name, JSON):
    """Convert JSON representation of a MIDI file to PyMus."""
    string = json.loads(JSON)
    noteTrack = 0
    previousTime = 0
    trackTime = 0
    for i in range(0, len(string.get("tracks"))):
        if len(string.get("tracks")[i].get("notes")) > 0:
            noteTrack = i
            break
    notes = string.get("tracks")[noteTrack].get("notes")
    pyMus = "NAME=" + name + "\nBEATLENGTH=1" + "\nSTART\n"
    for i in range(0, len(notes)):
        notename = notes[i].get("name")
        duration = int(round(notes[i].get("duration") * 1000))
        timediff = (notes[i].get("time") * 1000) - (previousTime + (notes[i].get("duration") * 1000))
        if timediff >= 100:
            pyMus += "- " + str(round(timediff)) + "\n"
        pyMus += notename + " " + str(duration) + "\n"
        previousTime = int(round(notes[i].get("time") * 1000))
    return pyMus


def play(pyMus):
    """Take the data from a PyMus file, and play it."""
    name = pyMus[0]
    beatlength = pyMus[1]
    song = pyMus[2]
    length = beatlength * len(song)
    print("Playing '" + name + "'\n\n")
    print("NOTE       DURATION")
    for i in range(0, len(song)):
        if song[i][0] == "":
            time.sleep(beatlength/1000)
            print("--         " + str(beatlength/1000).zfill(5))
        elif song[i][0] == "-":
            duration = int(round(float(song[i][1]) * beatlength))
            print("--         " + str(duration).zfill(5))
            time.sleep(duration/1000)
        else:
            note = song[i][0]
            duration = beatlength
            if len(song[i]) > 1:
                duration = int(round(float(song[i][1]) * beatlength))
            extrapadding = ""
            if len(note) < 10:
                extrapadding = (10 - len(note)) * " "
            print(song[i][0] + " " + extrapadding + str(duration).zfill(5))
            playNote(song[i][0], duration)

def oldmain():
    name = input("Please enter the name of the song, with no spaces: ")
    f = open(name + ".json","r")
    jsontext = f.read()
    f.close()
    thetext = parseJSON(name, jsontext)
    f = open(name + ".pymus", "w")
    f.write(thetext)
    f.close()
    play(readPyMus(name + ".pymus"))

def main():
    Tk().withdraw()
    filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("All Supported File Types", "*.pymus *.json"),("PyMus Files","*.pymus"),("JSON Files","*.json"),("All Files","*.*")))
    ext = filename.split(".")[-1]
    name = filename.split("/")[-1].split(".")[-2]
    if ext.lower() == "pymus":
        print("Playing PyMus file.")
        play(readPyMus(filename))
    elif ext.lower() == "json":
        save = messagebox.askyesno("JSON Conversion","You have selected a JSON file to be played.\nPyMus will attempt to convert this into PyMus notation.\nWould you like to save the converted PyMus file?\nIf you say no, the file will still be played, it just won't be saved.")
        f = open(filename, "r")
        jsondata = f.read()
        f.close()
        pyMus = parsePyMus(parseJSON(name, jsondata))
        if save == True:
            f = open(filename.replace(ext, "pymus"), "w")
            f.write(parseJSON(name, jsondata))
            f.close()
            print("JSON file converted and saved.")
        else:
            print("JSON file converted and discarded.")
        print("Playing converted JSON file. This file may not be fully compatible with PyMus.")
        play(pyMus)
        

main()
