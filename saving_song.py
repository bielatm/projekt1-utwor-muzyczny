import scipy.io.wavfile
import numpy


def write_song(dir, y):
    '''
    Zapisuje wektor y do pliku dir.wav
    '''
    scipy.io.wavfile.write(dir, 44100, numpy.int16(y/max(numpy.abs(y))*32767))
