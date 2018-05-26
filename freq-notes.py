notes-frequencies = [][]
a = 440.0 # a is 440 hz...

for x in range (126):
   midi.append( (a / 32.0) * (2.0 ** ((x - 9.0) / 12.0)))

print(midi)

