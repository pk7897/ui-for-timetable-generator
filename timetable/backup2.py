from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
import json

from .models import Classes,Groups

def index(request):
	request.session['existingGroup'] = False
	request.session['groupname'] = ""
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


'''def processClass(request,name):
	context = {}
	context['groups'] = []
	cn = request.POST['classname']
	
	c = Classes.objects.filter( cname = cn ).first()
	if c == None:
		C = Classes()
		C.cname = request.POST['classname']
		C.save()
		context['groups'] = C.grouplist()
	else:
		context['groups'] = Classes.objects.get(cname = cn).grouplist()
		
	request.session['existingClass'] = True
	request.session['classname'] = cn
	return render(request, 'timetable/addGroup.html', context)

	
def processClass(request,name):
	context = {}
	context['groups'] = []
	cn = request.POST['classname']
	
	c = Classes.objects.filter( cname = cn ).first()
	if c == None:
		C = Classes()
		C.cname = request.POST['classname']
		C.save()
		context['groups'] = C.grouplist()
	else:
		context['groups'] = Classes.objects.get(cname = cn).grouplist()
		
	request.session['existingClass'] = True
	request.session['classname'] = cn
	return render(request, 'timetable/addGroup.html', context)
'''	
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
	return render(request, 'timetable/processGroup.html', context)

	
def addSub(request,id):
	
	
	
def processSub(request):
	sub = request.POST['subname']
	g = Groups.objects.get(pk = id)
	myList = g.subjectlist()
	request.session['existingGroup'] = True
	request.session['groupname'] = g.grpname
	flag = 1
	for a in myList:
		if a.subname == sub:
			flag = 0
			break
	
	if flag:
		C = Classes.objects.get(cname = request.session['classname'])
		C.subj_list.create(subname = sub)
		C.save()
		g.sublist.create(subname = sub)
		g.save()
	
	return HttpResponse("You're at the polls index.")
