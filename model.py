import json
from jsonic import Serializable

class Subject(Serializable):
	"""docstring for Subject"""
	def __init__(self, sub_code, title, sub_priority=0, t_name="", is_practical=False ):
		super(Subject, self).__init__()

		self.t_name = t_name
		self.is_practical = is_practical
		self.title = title
		self.sub_code = str(sub_code)
		self.sub_priority = sub_priority

		self.tt_data = []
	
	def initTT(self,pref):
		self.tt_data = [[None for x in range(pref['t_period_pd'])] for _ in range(pref['t_day'])]

	def getData(self):
		return self.tt_data

	def __eq__(self,sub):
		if isinstance(sub,Subject):
			return sub.sub_code == self.sub_code
		else: return False

	def __str__(self):
		return self.title

	def __repr__(self):
		return self.title
	
	def toJson(self):
		return json.dumps(self.__dict__)

class Classroom(Serializable):
	"""docstring for Classroom"""
	def __init__(self, name, cls_code, tt_data=[], primary_sub=None):
		super(Classroom, self).__init__()
		
		self.name = name
		self.tt_data = tt_data
		self.cls_code = (cls_code)
		self.primary_sub = primary_sub

		self.sData = []

	def setData(self,d):
		self.tt_data = d

	def getData(self):
		return self.tt_data

class SubjectSet():
	def __init__(self,name,data):
		self.name = name
		self.data = data