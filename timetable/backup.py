from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
import json

from .models import Classes,Groups,Subjects,Faculty
def index(request):
	request.session['existingSubject'] = False
	request.session['existingGroup'] = False
	request.session['existingClass'] = False
	request.session['classname'] = ""
	context = {}
	context['classes'] = Classes.objects.all()
	return render(request, 'timetable/index.html',context)

def processClass(request):
	context = {}
	context['iserror'] = False
	cn = request.POST['classname']
	c = Classes.objects.filter( cname = cn ).first()
	if c == None:
		C = Classes()
		C.cname = request.POST['classname']
		C.save()
		context['message'] = "Class is successfully added."
	else:
		context['iserror'] = True
		context['message'] = "Class has already been added."
	
	return render(request, 'timetable/processClass.html', context)

def addGroup(request,name):
	request.session['existingClass'] = True
	request.session['classname'] = name
	context = {}
	C = Classes.objects.get(cname = name)
	context['groups'] = C.grouplist()
	return render(request, 'timetable/addGroup.html',context)

def processGroup(request):
	grp = request.POST['groupname']
	context = {}
	context['iserror'] = False
	context['classname'] = request.session['classname']
	C = Classes.objects.get(cname = request.session['classname'])
	g = C.grplist.filter(grpname = grp).first()
	if g == None:
		C.grplist.create(grpname = grp)
		C.save()
		context['message'] = "Group is successfully added."
	else:
		context['iserror'] = True
		context['message'] = "Group has already been added."

	return render(request, 'timetable/processGroup.html', context)

	
def addSubject(request,id):
	
	request.session['existingGroup'] = True
	request.session['groupid'] = id
	context = {}
	g = Groups.objects.get(pk = id)
	context['subjects'] = g.subjectlist()
	return render(request, 'timetable/addSub.html',context)

	
def processSub(request):
	sub = request.POST['subname']
	subt = request.POST['Sub_type']
	g = Groups.objects.get(pk = request.session['groupid'])
	s = g.sublist.filter(subname = sub).first()
	context = {}
	context['iserror'] = False
	context["groupid"] = request.session['groupid']
	if s == None:
		C = Classes.objects.get(cname = request.session['classname'])
		C.subj_list.create(subname = sub,subtype = subt )
		C.save()
		g.sublist.create(subname = sub,subtype = subt )
		g.save()
		context['message'] = "Subject is successfully added."
	else:
		context['iserror'] = True
		context['message'] = "Subject has already been added."

	return render(request, 'timetable/processSubject.html', context)
	
def addFaculty(request,id):
	request.session['existingSubject'] = True
	request.session['subjectid'] = id
	context = {}
	s = Subjects.objects.get(pk = id)
	context["subjectid"] = id
	context['faculties'] = s.facultylist()
	return render(request, 'timetable/addFac.html',context)
	
def processWH(request,id):
	wh = request.POST['wh']
	s = Subjects.objects.get(pk = id)

def processFaculty(request):	
	fac = request.POST['facname']
	s = Subjects.objects.get(pk = request.session['subjectid'])
	f = s.faclist.filter(facname = fac).first()
	context = {}
	context['check'] = False
	context['choice'] = False
	context["subjectid"] = request.session['subjectid']
	if f == None:
		l = len(s.facultylist())
		if l == 0:
			s.faclist.create(facname = fac)
			s.save()
			context['message'] ="Faculty is successfully added."
		else:
			context['check'] = True
			request.session['pending_fac'] = fac
	else:
		context['message'] = "Faculty has already been added."

	return render(request, 'timetable/processFaculty.html', context)

def multiple_faculty(request,id):
	context = {}
	context['check'] = False
	context["subjectid"] = id
	context['choice'] = False
	choice = request.POST['choice']
	if choice == "Yes":
		s = Subjects.objects.get(pk = id)
		s.faclist.create(facname = request.session['pending_fac'])
		s.save()
		context['message'] ="Faculty is successfully added."
	else:
		context['message'] ="Faculty is NOT added."
	return render(request, 'timetable/processFaculty.html', context)
	
def Generate(request):
	C = Classes.objects.get(cname = request.POST['gen'])
	g = C.grouplist()
	for gs in g:
		print ("*" + C.cname + "-" + gs.grpname)
		s = gs.subjectlist()
		for ss in s:
			print(ss.subname,end =':')
			f = ss.facultylist()
			l = len(f)
			for fs in range(l):
				if fs == l-1:
					print (f[fs].facname,sep=':')
				else:
					print (f[fs].facname,end=',')
					
	return HttpResponse("The required output is generated")
	
