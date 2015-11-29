# -*- coding: utf-8 -*-
"""
Modul create_songs zawiera podstawowe funkcje odpowiedzialne za generowanie
piosenek w programie beatbox.py. Skladaja sie na niego dwie funkcje:

* create_song(song_name):
Funkcja ta wczytuje podstawowe parametry song_nameu (okreslone w pliku defs.txt)
i liste sciezek, ktore skladaja sie na utwor (w pliku song.txt). Funkcja
zaklada, ze pliki w katalogu sa sformatowane poprawnie.

* create_track(track_id, song_name, defs):
Funkcja ta generuje pojedyncza sciezke na podstawie parametrow. Zwraca
rowniez ilosc wierszy w sciezce.

Szczegoly w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015
"""
import numpy as np
from add_notes import *
from add_samples import *

def create_song(song_name):
    """
    Funkcja create_song(song_name) tworzy utwor, ktorego parametry
    zapisane sa w katalogu o tej samej nazwie.
    """
    defs = eval(open(song_name + '/defs.txt', 'r').read())
    song_file = open(song_name + '/song.txt', 'r')
    rr = song_file.readline().rstrip('\n')
    
    song, lines = create_track(int(rr), song_name, defs)
    for file in song_file:
        
        song1, lines1 = create_track(int(file.rstrip('\n')), song_name, defs)
        song = np.append(song, 
                         np.zeros(lines1 * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"]), dtype = np.float)
                        )
        n0 = lines * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"])
        n1 = lines1 * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"])
        for n in range(n0, n0 + n1):
            song[n] = song[n] + song1[n - n0]
        lines = lines + lines1
    
    song_file.close()
    return song, defs["fs"]
    
def create_track(track_id, song_name, defs):
    """
    Funkcja create_track(track_id, song_name, defs) tworzy sciezke o numerze
    track_id, ktorej parametry zapisane sa w pliku trackXY.txt, gdzie 
    XY = track_id. Pozostale argumenty funkcji to nazwa katalogu, w ktorym
    znajduja sie parametry piosenki oraz slownik defs, ktory zawiera
    pola jak w pliku defs.txt.
    """
    track_file = open(song_name + '/track{:02}.txt'.format(track_id), 'r')
    track_lines = [track_file.readline().rstrip('\n')]
    for line in track_file:
        track_lines = np.append(track_lines, line)
    track_file.close()
    
    
    time = len(track_lines) * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"])
    l = (len(track_lines[0]) - defs["tracks"] + 1) // defs["tracks"]
    if defs["sample_type"] == 'sample':
        track = np.zeros(time, dtype = np.int32)   
    elif defs["sample_type"] == 'notes':
        track = np.zeros(time, dtype = np.float)
    for i in range(len(track_lines)):
        for t in range(defs["tracks"]):
            if track_lines[i][t * (l + 1)] != '-':
                if defs["sample_type"] == 'sample':
                    sample_id = int(track_lines[i][t * (l + 1):t * (l + 1) + l])
                    track = add_sample(track, sample_id, i, song_name, defs)
                if defs["sample_type"] == 'notes':
                    note_name = track_lines[i][(t * (l + 1)+3):(t * (l + 1) + 6)]
                    instrument_id = track_lines[i][(t * (l + 1)+0):(t * (l + 1) + 2)]
                    
                    note = create_note(instrument_id, note_name, 2 * int(track_lines[i][(t * (l + 1)+7):(t * (l + 1) + 9)]) * 60 / (defs["bpm"] * defs["rpb"]), song_name, defs)
                    track = add_note(track, note, i, defs)
                
    return track, len(track_lines)