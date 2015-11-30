import json
import numpy
import scipy.io.wavfile
import zipfile


def read_zip_files(dir):

    '''
    Z plik dir (z roszerzeniem .zip) wczytuje dane z plików txt do:
    s - song.txt jako lista
    bpm - parametr z pliku defs.txt
    uniqs - slownik unikalnych elementow z s wraz z ich licznoscia
    tracks - slownik unikalnych elementow z s i lista list granych sampli
    '''

    archive = zipfile.ZipFile(dir, 'r')

    with archive.open('defs.txt') as json_file:
        bpm = json.loads(json_file.read().decode('ascii'))['bpm']

    with archive.open('song.txt') as song:
        s = [e[:-1].decode('ascii') for e in song.readlines()]

    uniqs = {k: s.count(k) for k in set(s)}

    tracks = {}
    for e in uniqs.keys():
        with archive.open('track{0}.txt'.format(e)) as track:
            tracks[e] = [e[:-2].decode('ascii').split(" ") for e in track.readlines()]

    return s, bpm, uniqs, tracks


def read_files(dir):

    '''
    Z katalogu dir wczytuje dane z plików txt do:
    s - song.txt jako lista
    bpm - parametr z pliku defs.txt
    uniqs - slownik unikalnych elementow z s wraz z ich licznoscia
    tracks - slownik unikalnych elementow z s i lista list granych sampli
    '''

    with open('{0}defs.txt'.format(dir)) as json_file:
        bpm = json.load(json_file)['bpm']

    with open('{0}song.txt'.format(dir), 'r') as song:
        s = [e[:-1] for e in song.readlines()]

    uniqs = {k: s.count(k) for k in set(s)}

    tracks = {}
    for e in uniqs.keys():
        with open('{0}track{1}.txt'.format(dir, e), 'r') as track:
            tracks[e] = [e[:-1].split(" ") for e in track.readlines()]
    return s, bpm, uniqs, tracks


def sound(fs, bpm, note_no, gama):

    '''
    Zapisuje nute jako wektor o czestotliwosci fs, dlugosci 60/bpm.
    note_no - odleglosc danej nuty od A-4, gama - gama, z ktrorej gramy nute
    '''

    t = numpy.linspace(0, 60/bpm, 60/bpm*fs)
    y = numpy.sin(2*numpy.pi*440*pow(2, 1/12)**(2*note_no)*gama*t)
    return y


def create_song(s, bpm, uniqs, tracks, notes, dir):

    '''
    Zapisuje piosenke jako wektor.
    Przyjmuje parametry:
    s - song.txt jako lista
    bpm - parametr z pliku defs.txt
    uniqs - slownik unikalnych elementow z s wraz z ich licznoscia
    tracks - slownik unikalnych elementow z s i lista list granych sampli
    notes - slownik nut wraz z ich odlegloscia od A-4
    dir - katalog, w ktorym znajduja sie sample
    '''

    tracklines = {k: len(v) for k, v in tracks.items()}

    y = numpy.zeros(int(60/bpm*44100)*sum(uniqs[k]*tracklines[k] for k in uniqs.keys()))

    k = -1
    for e in s:
        for f in tracks[e]:
            k += 1
            for g in f:
                if g[0] in notes.keys():
                    note_no = notes[g[0]] + 0.5 if g[1] == '#' else notes[g[0]]
                    tmp = sound(44100, bpm, note_no, int(g[2])-4+1)
                    y[int(60/bpm*44100*k):int(60/bpm*44100*k) + len(tmp)] += tmp
                elif g == '--':
                    pass
                else:
                    pom = scipy.io.wavfile.read('{0}sample{1}.wav'.format(dir, g))[1]
                    pom = numpy.mean(pom, axis=1) / 32767
                    y[int(60/bpm*44100*k):int(min(60/bpm*44100*k + len(pom), len(y)))] += \
                        pom[0:int(min(60/bpm*44100*k + len(pom), len(y))) - int(60/bpm*44100*k)]
    return y


def create_zip_song(s, bpm, uniqs, tracks, notes, samples):

    '''
    Zapisuje piosenke jako wektor.
    Przyjmuje parametry:
    s - song.txt jako lista
    bpm - parametr z pliku defs.txt
    uniqs - slownik unikalnych elementow z s wraz z ich licznoscia
    tracks - slownik unikalnych elementow z s i lista list granych sampli
    notes - slownik nut wraz z ich odlegloscia od A-4
    samples - nazwy plikow tymczasowych, w ktorych przechowywane sa sample
    '''

    tracklines = {k: len(v) for k, v in tracks.items()}

    y = numpy.zeros(int(60/bpm*44100)*sum(uniqs[k]*tracklines[k] for k in uniqs.keys()))

    k = -1
    for e in s:
        for f in tracks[e]:
            k += 1
            for g in f:
                if g[0] in notes.keys():
                    note_no = notes[g[0]] + 0.5 if g[1] == '#' else notes[g[0]]
                    tmp = sound(44100, bpm, note_no, int(g[2])-4+1)
                    y[int(60/bpm*44100*k):int(60/bpm*44100*k) + len(tmp)] += tmp
                elif g == '--':
                    pass
                else:
                    pom = scipy.io.wavfile.read(samples[g])[1]
                    pom = numpy.mean(pom, axis=1) / 32767
                    y[int(60/bpm*44100*k):int(min(60/bpm*44100*k + len(pom), len(y)))] += \
                        pom[0:int(min(60/bpm*44100*k + len(pom), len(y))) - int(60/bpm*44100*k)]
    return y
