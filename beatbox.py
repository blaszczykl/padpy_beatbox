#!/opt/anaconda/bin/ipython
"""
Program beatbox.py generuje na podstawie katalogu lub archiwum .zip podanego
jako argument piosenke o takiej samej nazwie (pli .wav). Zawartosc katalogu
lub archiwum musi spelniac wymagania opisane w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015
"""
import os.path
import sys
import zipfile
import tempfile
from create_songs import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Choose a song!")
    else:
        song_name = os.path.basename(sys.argv[1])
        if os.path.isdir(song_name):
            if song_name.endswith('/'):
                song_name = song_name[:-1]
            track, fs = create_song(song_name)
            scipy.io.wavfile.write(song_name + '.wav', fs, np.int16(track/max(np.abs(track))*32767))
            print("File "+song_name+".wav created.")
        elif zipfile.is_zipfile(song_name) or zipfile.is_zipfile(song_name+'.zip'):
            directory_name = tempfile.mkdtemp()
            if song_name.endswith('.zip'):
                song_name = song_name[:-4]
            zf = zipfile.ZipFile(song_name+'.zip')
            zf.extractall(path=directory_name)
            track, fs = create_song(directory_name)
            scipy.io.wavfile.write(song_name + '.wav', fs, np.int16(track/max(np.abs(track))*32767))
            print("File "+song_name+".wav created.")
        else:
            print("Wrong song name!")