import os

s = 'The.Avengers.Earths.Mightiest.Heroes.S02E16.720p.BluRay.x264-DEiMOS'
# RESTART HERE
s2 =  ' '.join(s.split('.')[:-1]) + '.' + s.split('.')[-1]


print(s2)