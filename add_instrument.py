# -*- coding: utf-8 -*-
"""
Modul add_instrument zawiera funkcje generujace fale imitujace instrument
zdefiniowany przez uzytkownika w pliku sampleXY. Modul zawiera
trzy funkcje:

* wave_fun(t, fun)
Funkcja ta wybiera jakiego rodzaju fali uzyc (sinusoidalnej, trojkatnej czy
prostokatnej).

* create_wave(t, freq, wave)
Funkcja ta tworzy fale o odpowiednich parametrach.

* create_envelope(t, freq, wave, defs)
Funkcja ta tworzy obwiednie fali o odpowiednim czasie narastania, opadania
itd.

Szczegoly w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015
"""
import numpy as np
import scipy.signal as sp

def wave_fun(t, fun):
    """
    Funkcja wave_fun(t, fun) definiuje funkcje, jaka ma wykonac na zmiennej t.
    Argument fun moze przyjmowac 3 wartosci - sin, saw i rec, wowczas generuje
    fale sinusoidalna, trojkatna lub prostokatna, odpowiednio.
    """
    if fun == 'sin':
        return np.sin(t)
    elif fun == 'saw':
        return sp.sawtooth(t)
    elif fun == 'rec':
        return np.sign(np.sin(t))

def create_wave(t, freq, wave):
    """
    Funkcja create_wave(t, freq, wave) tworzy fale (na wektorze zmiennej
    niezaleznej t) o czestotliwosci freq i parametrach danych w zmiennej
    wave (slowniku). Szczegoly dotyczace zawartosci slownika w pliku 
    readme.txt.
    """
    if type(wave["wave"]) is str:
        return wave["ampl"] * wave_fun(wave["freq"] * 2 * np.pi * freq * t + wave["phas"], wave["wave"]) ** wave["expo"]
    elif type(wave["wave"]) is list:
        n = len(wave["wave"])
        N = len(t)
        mod = np.zeros(N)
        for i in range(1, n):
            mod = mod + wave["ampl"][i] * wave_fun(wave["freq"][i] * 2 * np.pi * freq * t + wave["phas"][i], wave["wave"][i]) ** wave["expo"][i]
        return wave["ampl"][0] * wave_fun(wave["freq"][0] * 2 * np.pi * freq * t + wave["phas"][0] + mod, wave["wave"][0]) ** wave["expo"][0]
        
def create_envelope(t, freq, wave, defs):
    """
    Funkcja create_envelope(t, freq, wave, defs) tworzy obwiednie fali (na
    wektorze zmiennej niezaleznej t) o czestotliwosci freq o parametrach
    danych w slownikach wave i defs. Szczegoly dotyczace zawartosci slownikow
    w pliku readme.txt.
    """
    a = np.floor(wave["attack"] * t[-1] * defs["fs"])
    Att = np.linspace(0, 1, a)
    
    # decay
    d = np.floor(wave["decay"] * t[-1] * defs["fs"])
    
    if wave["dampen"] == 'log':     # imitating piano
        dampen = (0.5 * np.log(freq * d / defs["fs"])) ** 2
    elif wave["dampen"] == 'lin':   # imitating organ
        dampen = 1 + freq * 0.01
    
    Dec = np.linspace(1, wave["sustain"], d) ** dampen
    
    # release
    r = np.floor(wave["release"] * t[-1] * defs["fs"])
    Rel = np.linspace(wave["sustain"], 0, r)
    
    # sustain
    Sus = wave["sustain"] * np.ones(t[-1] * defs["fs"] - a - d - r)
    
    return np.hstack((Att, Dec, Sus, Rel))