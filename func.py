
import random
import uuid
import collections

from click import File

from model import *

def genKey(key=None):
	if not key: key = str(uuid.uuid4())[:4]
	random.seed(key)

def generateClass(pref):
	# cls_data -> [{'n':"",'tt':[]}, {},{}]
	rf = [Classroom("XII A", '001'), Classroom("XII B",'002'), Classroom("XII C",'003')]
	for i in rf:
		i.tt_data = [[] for _ in range(pref['t_day'])]
	return rf

def clearData(clsr,pref):
	for i in clsr:
		i.tt_data = [[] for _ in range(pref['t_day'])]
	return clsr

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
	lt = collections.deque([],len(clsr)+2)

	# Adding periods to classes
	for i in range(pref['t_period_pd']):
		for x in range(pref['t_day']):
			for y in clsr:
				for _ in range(len(clsr)+10):
					tr = random.choice(y.sData)
					if tr.sub_code not in lt or (i == (pref['t_period_pd']-1) and x == (pref['t_day']-1)):
						break
					# Checking if number of periods for a subject per day per class is exceeding the threshold
					if sum(1 for p in y.tt_data[x] if p.sub_code == tr.sub_code) < 3:
						break
				y.sData.remove(tr) # Removing the selected subject from sample list
				y.tt_data[x].append(tr) # Adding Subject to corresponding timetable field
				sb[tr.sub_code].tt_data[x][i] = y # Linking class to subject for faculty timetable
				lt.append(tr.sub_code) # Adding to deque
	return clsr,sb
