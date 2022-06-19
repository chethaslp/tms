
import random
import uuid
import collections

from click import File

from model import *

# Sets Key for random function seed.
# Randomness can be controlled using seed and helps to get same values everytime.
def genKey(key=None):
	if not key: key = str(uuid.uuid4())[:4]
	random.seed(key)

def generateClass(pref):
	rf = [Classroom("XII A", '001'), Classroom("XII B",'002'), Classroom("XII C",'003')]
	for i in rf:
		i.tt_data = [[] for _ in range(pref['t_day'])]
	return rf

def clearData(clsr,pref):
	for i in clsr:
		i.tt_data = [[None for _ in range(pref['t_period_pd'])] for _ in range(pref['t_day'])]
	return clsr

# - Timetable sort Algorithm -
# params -> pref{}: Dict of constant vars
# 			clsr[]: List of classes
# 			sub[] : List of subjects
# Init -> creates a sample DB sData[], appends "Subject" for (sub_priority * No: of classes) times into sData[]
# Process -> Gets a random "Subject" from sData, check if it matches the given timetable colunm and other criterions(*), if not chooses another "Subject" randomly (repeats process till condition satifies.)
# returns -> clsr[]: List of classes with sorted Timetable
# 			 sb{}: Dict of subjects with sorted Timetable [Faculty Timetable]
def gen_tt(pref, clsr, sub):
	sb= {}
	tr = None

	clsr = clearData(clsr,pref)

	# Initializing Sample Data
	for u in sub:
		for h in range(u.sub_priority):
			for i in clsr:
				i.sData.append(u)
		u.initTT(pref)
		sb[u.sub_code] = u

	# Dequeue for dismissing period repetition
	lt = collections.deque([],len(clsr)*2)

	# Adding periods to classes
	for i in range(pref['t_period_pd']):
		for x in range(pref['t_day']): 
			for y in clsr:
				for _ in range(100):
					if i==0 and y.primary_sub:
						tr= y.primary_sub
						break
					else: 
						tr = random.choice(y.sData)
						if tr.sub_code in lt: continue
						if (i == (pref['t_period_pd']-1) and x == (pref['t_day']-1)): break

						# Checking if number of periods for a subject per day per class is exceeding the threshold
						if sum(1 for p in y.tt_data[x] if p and p.sub_code == tr.sub_code) < 3:
							break
				y.sData.remove(tr) # Removing the selected subject from sample list
				y.tt_data[x][i] = tr # Adding Subject to corresponding timetable field
				sb[tr.sub_code].tt_data[x][i] = y # Linking class to subject for faculty timetable
				lt.append(tr.sub_code) # Adding to deque
	return clsr,sb

# Timetable sort Algorithm 2 
# OBSOLETE. Algo requires refracting and has logical errors. Sticking with algo 1.
def gen_tt2(pref, clsr, sub):
	sb= {}
	tr = None

	clsr = clearData(clsr,pref)
	# Initializing Sample Data
	for u in sub:
		for h in range(u.sub_priority):
			for i in clsr:
				i.sData.append(u)
		u.initTT(pref)
		sb[u.sub_code] = u

	for c in clsr:
		for tr in c.sData:
			while True:
				x = random.randrange(0,pref['t_day'])
				y = random.randrange(0,pref['t_period_pd'])
				if not c.tt_data[x][y]:
					break
				if (y+1 != pref['t_period_pd']) and c.tt_data[x][y+1] and c.tt_data[x][y+1].sub_code == tr.sub_code: continue
				if (y-1 != -1) and c.tt_data[x][y-1] and c.tt_data[x][y-1].sub_code == tr.sub_code: continue

				if len([c2 for c2 in clsr if c2.tt_data[x][y] and c2.tt_data[x][y].sub_code == tr.sub_code]) != 0: continue
				break 
			c.tt_data[x][y] = tr
			sb[tr.sub_code].tt_data[x][y] = c
	return clsr,sb

			 
	
