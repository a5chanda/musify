from __future__ import division

#! /usr/bin/env python
import math
from math import log2, pow
import sys
from aubio import source, tempo
import json
from numpy import median, diff
import matplotlib.pyplot as plt


def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            print("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break
    return beats

def beats_to_bpm(beats, path):
    # if enough beats are found, convert to periods then to bpm
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        return median(bpms)
    else:
        print("not enough beats found in {:s}".format(path))
        return 0

def key(arr):
    import music21 as music
    s1 = music.stream.Stream()
    for i in arr:
      s1.append(music.note.Note(i, type="quarter"))

    return music.analysis.discrete.analyzeStream(s1, 'key')


#if len(sys.argv) < 2:
#    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
#    sys.exit(1)
def init(filename):
	from aubio import pitch
	beats = get_file_bpm(filename)
	bpm = beats_to_bpm(beats, filename)
	beat_count = len(beats)
	print(bpm)

	downsample = 1
	samplerate = 44100 // downsample
	if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

	win_s = 4096 // downsample # fft size
	hop_s = 512  // downsample # hop size

	s = source(filename, samplerate, hop_s)
	samplerate = s.samplerate

	tolerance = 0.8

	pitch_o = pitch("yin", win_s, hop_s, samplerate)
	pitch_o.set_unit("Hz")
	pitch_o.set_tolerance(tolerance)

	pitches = []
	confidences = []

	# total number of frames read
	total_frames = 0
	pitches2 = []
	times = []
	while True:
	    samples, read = s()
	    pitch = pitch_o(samples)[0]
	    #pitch = int(round(pitch))
	    confidence = pitch_o.get_confidence()
	    #if confidence < 0.8: pitch = 0.
	    pitches2.append(pitch)
	    times.append(total_frames / float(samplerate))
	    #print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
	    pitches += [pitch]
	    confidences += [confidence]
	    total_frames += read
	    if read < hop_s: break

	l = len(times)/beat_count
	arr = []
	count = 0
	temp = []

	import itertools
	import operator

	def roundArray(arr):
	    for i in arr:
	        round(i)

	def most_common(L):
	  # get an iterable of (item, iterable) pairs
	  SL = sorted((x, i) for i, x in enumerate(L))
	  # print 'SL:', SL
	  groups = itertools.groupby(SL, key=operator.itemgetter(0))
	  # auxiliary function to get "quality" for an item
	  def _auxfun(g):
	    item, iterable = g
	    count = 0
	    min_index = len(L)
	    for _, where in iterable:
	      count += 1
	      min_index = min(min_index, where)
	    # print 'item %r, count %r, minind %r' % (item, count, min_index)
	    return count, -min_index
	  # pick the highest-count/earliest item
	  return max(groups, key=_auxfun)[0]

	for i in pitches2:
	    if count < l:
	        count += 1
	        if i >= 300 and i <= 1100:
	            temp.append(i)
	    else:
	        if len(temp) > 0:
	            roundArray(temp)
	            arr.append(most_common(temp))
	        temp = []
	        count = 0

	C0 = 440.0*math.pow(2, -4.75)
	name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

	def pitch(freq):
	    h = round(12*log2(freq/C0))
	    octave = h // 12
	    n = h % 12
	    return name[n] + str(octave)

	notes = []

	for i in arr:
	    notes.append(pitch(i))

	print(notes)
	data = {}
	mkey = key(notes)
	data['key'] = str(mkey)
	data['notes'] = notes
	data['bpm'] = bpm
	#data['key'] = mkey
	data['beat_count'] = beat_count
	json_data = json.dumps(data)
	return json_data