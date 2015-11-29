PROGRAM BEATBOX.PY
autor: Lukasz Blaszczyk
modyfikacje: 29 listopada 2015

1. Wywolanie funkcji:
./beatbox.py <nazwa_utworu>
gdzie <nazwa_utworu> moze byc zarowno nazwa katalogu, w ktorym umieszczone
sa parametry utworu, a także nazwa archiwum .zip, ktory te parametry zawiera.
Uwaga: moze byc konieczna zmiana sciezki do zainstalowanej dystrybucji
Pythona. Aktualnie jest: /opt/anaconda/bin/ipython

2. Mozliwosci:
Program tworzy piosenke na podstawie parametrow umieszczonych w katalogu
<nazwa_utworu>. Możliwe jest umieszczenie w katalogu gotowych sampli (w postaci
plików sampleXY.wav) i polaczenia ich w sciezki, a takze zdefiniowanie
wlasnego instrumentu i odtworzenie utworu na podstawie nut.

A. Utwor na podstawie sampli
W katalogu <nazwa_utworu> nalezy umiescic pliki sampleXY.wav, bedace gotowymi
samplami (numeracja XY - 01, 02, 03, ... - numery dwucyfrowe). W pliku
song.txt nalezy podac liste sciezek jakie skladaja sie na utwor, tzn. kolumne
z liczbami UV, gdzie UV to numery z plikow trackUV.txt, np.
01
02
01
01

Plik trackUV.txt (numeracja UV - 01, 02, 03, ... - numery dwucyfrowe) zawiera
numery sampli umieszczone w kolejnych wierszach. Mozliwe jest podanie 
kilku kolumn sampli (w kazdym wierszu musi byc identyczna liczba kolumn):
01 02
01 --
03 --
01 --
01 02
01 --
03 --
01 --

Wpisanie "--" oznacza pauze. W katalogu nalezy umiescic rowniez plik 
defs.txt postaci
{
    "bpm": 80,
    "rpb": 2,
    "tracks": 2,
    "sample_type": 'sample',
    "fs": 44100
}
gdzie "bmp" oznacza ilosc beatow na minute, "rpb" oznacza ilosc linii (w 
plikach trackUV.txt) na jeden beat, "tracks" to liczba wierszy w kolumnach,
"sample_type" w tym przypadku musi byc rowne 'sample', a "fs" to czestotliwosc
probkowania w pliku .wav.

B. Utwor na podstawie nut
W katalogu <nazwa_utworu> nalezy umiescic pliki sampleXY.txt (numeracja jak 
wczesniej). W każdym z takich plikow nalezy zdefiniowac parametry instrumentu,
tzn. wpisac slownik:
{
    "wave": ['sin', 'sin', 'sin', 'sin'],
    "ampl": [1, 1, 0.5, 0.25],
    "expo": [1, 2, 1, 1],
    "freq": [2, 1, 1, 1],
    "phas": [0, 0, 0.25, 0.5],
    "attack": 0.3,
    "decay": 0.7,
    "dampen": 'lin',
    "sustain": 0,
    "release": 0
}
Fala dzwiekowa, jaka zostanie utworzona to
A0 * f0(freq0 * 2pi * t + phas0 
           + A1 * f1(freq1 * 2pi * t + phas1) ^ ex1
		   + A2 * f2(freq2 * 2pi * t + phas2) ^ ex2
		   + ...
		   + An * fn(freqn * 2pi * t + phasn) ^ exn) ^ ex0
Pole "wave" zawiera wektor (badz jedna wartosc) [f0, f1, f2, ..., fn],
gdzie fi moze przyjmowac wartosci:
- 'sin' - utworzy fale sinusoidalna,
- 'rec' - utworzy fale prostokatna,
- 'saw' - utworzy fale trojkatna.
Pole "ampl" zawiera wektor [A0, A1, A2, ..., An], pole "expo" wektor
[ex0, ex1, ex2, ..., exn], pole "freq" wektor [freq0, freq1, freq2, ...,
freqn], a pole "phas" wektor [phas0, phas1, phas2, ..., phasn].
Podstawowa fala zmoduluje obwiednie, zawierajaca 4 etapy: atak, spadek, 
przetrzymanie i wygaszenie, jak na obrazku:
  /\
 /  \_____
/         \
i slownik definiuje: pole "attack" to ulamek czasu trwania dzwieku 
przeznaczony na atak, "decay" to ulamen czasu przeznaczony na spadek, "dampen"
definiuje charakter spadku - mozliwe sa dwie opcje: 'lin' (spadek liniowy)
oraz 'log' (spadek logarytmiczny), zdefiniowane w programie, "sustain"
okresla na jakim poziomie bedzie przetrzymanie (liczba od 0 do 1), a "release"
okresla ulamek czasu przeznaczony na wygaszenie.
W pliku song.txt nalezy podac liste sciezek jakie skladaja sie na utwor, 
tzn. kolumne z liczbami UV, gdzie UV to numery z plikow trackUV.txt, np.
01
02
01
01

Plik trackUV.txt (numeracja UV - 01, 02, 03, ... - numery dwucyfrowe) zawiera w kolejnych kolumnach nuty w formacie:
XY:N-K:MN
gdzie XY to numer instrumentu (jak w pliku sampleXY.txt), N-K to nazwa nuty
(np. A-4), a MN to czas trwania nuty (w wierszach, np. 04 - dzwiek bedzie 
trwal przez 4 wiersze). Mozliwe jest podanie kilku kolumn nut (w kazdym
 wierszu musi byc identyczna liczba kolumn). Wpisanie "--" oznacza pauze:
01:D#2:04 --------- 01:F#4:01 01:A#4:01
--------- --------- 01:A-4:01 ---------
--------- --------- 01:F#4:02 01:A#4:02
--------- --------- --------- ---------
 
W katalogu nalezy umiescic rowniez plik defs.txt postaci takiej jak wczesniej,
pole "sample_type" musi byc rowne 'notes'.

3. Uwagi:
Program zaklada pelna wspolprace z uzytkownikiem - pliki musza byc podane
w takiej formie jak jest to zalozone i opisane wyzej.
