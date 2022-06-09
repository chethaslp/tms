
import random
import uuid
import collections

from click import File

from model import *

def genKey(key=None):
	if not key: key = str(uuid.uuid4())[:4]
	random.seed(key)


def generateClass(cls_data,pref):
	# cls_data -> [{'n':"",'tt':[]}, {},{}]
	rf = []
	for i in cls_data:
		r = [ [] for _ in range(pref['t_day'])]
		rf.append(Classroom(i['n'], r))
	return rf

def gen_tt(pref, clsr, sub):
	clsr = generateClass(clsr, pref)
	s = []
	tr = None

	for u in sub:
		for h in range(u.sub_priority):
			for i in clsr:
				i.sData.append(u)
	lt = collections.deque([],len(clsr))

	for i in range(0,pref['t_period_pd']):
		for x in range(0,pref['t_day']):
			for y in clsr:
				for _ in range(len(clsr)):
					tr = random.choice(y.sData)
					if tr.sub_code not in lt or (i == (pref['t_period_pd']-1) and x == (pref['t_day']-1)):
						break
				y.sData.remove(tr)
				y.tt_data[x].append(tr)
				lt.append(tr.sub_code)
	return clsr

