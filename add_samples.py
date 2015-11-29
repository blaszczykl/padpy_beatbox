# -*- coding: utf-8 -*-
"""
Modul add_samples zawiera funkcje wczytujaca gotowe sample z plikow .wav 
oraz dodajace je do istniejacej sciezki. Modul zawiera jedna funkcje: 
add_sample.

Szczegoly w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015
"""
import numpy as np
import scipy.io.wavfile

def add_sample(track, sample_id, position, song_name, defs):
    """
    Funkcja add_sample(track, sample_id, position, song_name, defs) dodaje do
    sciezki zapisanej w zmiennej track dzwiek zapisany w samplu sampleXY.wav,
    gdzie XY = sample_id. Dzwiek jest dodawany na pozycji (w wektorze
    zawierajacym sciezke) danej zmienna position. Pozostale argumenty funkcji 
    to nazwa katalogu, w ktorym znajduja sie parametry piosenki oraz slownik 
    defs, ktory zawiera pola jak w pliku defs.txt.
    """
    n0 = position * 60 * defs["fs"] // (defs["bpm"] * defs["rpb"])
    
    f, sample = scipy.io.wavfile.read(song_name + '/sample{:02}.wav'.format(sample_id))
    if sample.shape[1] == 2:
        sample = np.int32(np.mean(sample, axis = 1))
        
    d = n0 + len(sample) - len(track)
    if d > 0:
        track = np.append(track, np.zeros(d, np.int32))
    for n in range(n0, n0 + len(sample)):
        track[n] = track[n] + sample[n - n0]
    return track