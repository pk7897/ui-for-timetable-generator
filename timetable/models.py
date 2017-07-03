from django.db import models

class Faculty(models.Model):
	facname = models.CharField(max_length=120)
	
class Subjects(models.Model):
	subname = models.CharField(max_length=100)
	subtype = models.CharField(max_length=20, default = "Normal")
	faclist = models.ManyToManyField(Faculty)
	hours = models.IntegerField(default=0)
	added = models.BooleanField(default = False)
	whpd = models.CharField(max_length=200,default = "")
	whpd_check = models.BooleanField(default = False)
	slots = models.CharField(max_length=200,default = "")
	slot_check = models.BooleanField(default = False)
	
	def facultylist(self):
		return list(self.faclist.all())

class Groups(models.Model):
	grpname = models.CharField(max_length=100)
	sublist = models.ManyToManyField(Subjects)
	
	def subjectlist(self):
		return list(self.sublist.all())

class Classes(models.Model):
	cname = models.CharField(max_length=5)
	grplist = models.ManyToManyField(Groups)
	subj_list = models.ManyToManyField(Subjects)

	def grouplist(self):
		return list(self.grplist.all())
	
	def subjectlist(self):
		return list(self.subj_list.all())

