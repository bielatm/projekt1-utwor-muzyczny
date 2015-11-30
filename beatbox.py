#!/usr/bin/env python3
import sys
import saving_song
import loading_files
import zipfile
import tempfile
import re

notes = {
    'C': -4.5,
    'D': -3.5,
    'E': -2.5,
    'F': -2,
    'G': -1,
    'A': 0,
    'H': 1
}

if sys.argv[1][-4:] == '.zip':

    s, bpm, uniqs, tracks = loading_files.read_zip_files('{0}'.format(sys.argv[1]))

    samples = {}
    zip_file = zipfile.ZipFile(sys.argv[1])
    for name in zip_file.namelist():
        match = re.search('^sample(\d+)\.wav$', name)
        if match:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(zip_file.open(name).read())
                samples[match.group(1)] = tmp.name

    y = loading_files.create_zip_song(s, bpm, uniqs, tracks, notes, samples)
    saving_song.write_song('{0}.wav'.format(sys.argv[1][:-4]), y)

else:
    s, bpm, uniqs, tracks = loading_files.read_files('{0}'.format(sys.argv[1]))
    y = loading_files.create_song(s, bpm, uniqs, tracks, notes, '{0}'.format(sys.argv[1]))
    saving_song.write_song('{0}.wav'.format(sys.argv[1][:-1]), y)
