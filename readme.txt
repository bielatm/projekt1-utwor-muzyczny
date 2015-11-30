Program służy do generowania własnych piosenek lub dźwięków.

Plik główny beatbox.py uruchamiany z konsoli.

W katalogach: W_murowanej_piwnicy, Szla_dzieweczka_do_laseczka i Love_me_like_you_do podane są przykładowe definicje utworu, które uruchamiamy z konsoli wpisując ./beatbox.py nazwa_katalogu/

Piosenka o nazwie takiej jak podany katalog zapisuje się w katalogu głównym projektu.

Piosenki definiowane są za pomocą następujących plików tekstowych:
defs.txt - definiuje wartość bpm (beats per minute)
song.txt - określa kolejność odgrywania tracków.
trackAB.txt - definiuje odgrywaną ścieżkę, może zawierać nazwy nut (w formacie A-4 lub A#4 gdzie A - nazwa nuty, 4 - numer gamy, # - podnosi dany dźwięk o pół tonu) lub numery sampli (w postaci 00 - numer sampla, -- oznacza pauzę)
W każdym katalogu piosenki znajdują się też pliki .wav z samplami, jeśli te są używane w danej piosence.

Istnieje możliwość "odgrywania" spakowanych plików. W spakowanym pliku muszą znajdować się bezpośrednio pliki definiujące utwor. Uruchamiamy z konsoli wpisując ./beatbox.py nazwa_pliku.zip

