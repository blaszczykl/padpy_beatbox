# -*- coding: utf-8 -*-
"""
Modul add_notes zawiera funkcje tworzace dzwiek o okreslonej czestotliwosci
(nutke) imitujacy zdefiniowany przez uzytkownika instrument. Modul zawiera
dwie funkcje:

* create_note(instrument_id, note_name, time, song_name, defs)
Funkcja ta tworzy pojedyncza nutke.

* add_note(track, note, position, defs)
Funkcja ta dodaje nutke (gotowy dzwiek) do istniejacej sciezki.

Szczegoly w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015
"""
import numpy as np
from add_instrument import *

def add_note(track, note, position, defs):
    """
    Funkcja add_note(track, note, position, defs) dodaje do sciezki track
    nutke dana jako wektor note w pozycji position. Argument defs to slownik, 
    ktory zawiera pola jak w pliku defs.txt.
    """
    n0 = position * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"])
    
    d = n0 + len(note) - len(track)
    if d > 0:
        track = np.append(track, np.zeros(d, np.int32))
    for n in range(n0, n0 + len(note)):
        track[n] = track[n] + note[n - n0]
    return track
    
def create_note(instrument_id, note_name, time, song_name, defs):
    """
    Funkcja create_note(instrument_id, note_name, time, song_name, defs) tworzy
    nutke o nazwie note_name (np. A-4) imitujaca instrument o numerze
    instrument_id, ktorego parametry okreslone sa w pliku sampleXY.txt, gdzie
    XY = instrument_id, trwajaca czas time. Pozostale argumenty funkcji to nazwa katalogu, w ktorym
    znajduja sie parametry piosenki oraz slownik defs, ktory zawiera
    pola jak w pliku defs.txt.
    """
    notes = eval(open('notes.txt', 'r').read())
    if instrument_id == '00':
        wave = {"wave": 'sin', "ampl": 1, "expo": 1, "freq": 1, "phas": 0, "attack": 0.2, "decay": 0.0, "dampen": 'lin', "sustain": 1, "release": 0.3}
    else:
        wave = eval(open(song_name + '/sample' + instrument_id + '.txt', 'r').read())
    half = np.power(2, 1/12)
    fre0 = 440
    power = ((int(note_name[2])-1)*12 + notes[note_name[0:2]]) - ((4-1)*12 + notes["A-"]) 
    freq = fre0 * (half ** power)
    
    t = np.linspace(0, time, time * defs["fs"])
    
    Sin = create_wave(t, freq, wave)    
    mod = create_envelope(t, freq, wave, defs)
    
    return mod * Sin