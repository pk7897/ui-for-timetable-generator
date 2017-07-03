from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate

from .models import Classes,Groups,Subjects,Faculty
def index(request):
	request.session['existinggroup'] = False
	request.session['existingclass'] = False
	request.session['classname'] = ""
	request.session['indnorm'] = False
	request.session['unmapfac'] = False
	context = {}
	context['classes'] = Classes.objects.all()
	context['indclass'] = True
	context['indsub'] = False
	context['indfac'] = False
	return render(request, 'timetable/index.html',context)
	
def processindex(request,id):
	context = {}
	if id == "2":
		context['indclass'] = False
		context['indsub'] = True
		context['indfac'] = False
		C_M = Classes.objects.filter(cname = "Unmapclass").first()
		if C_M == None:
			context['subs'] = None
		else:
			C2 = Classes.objects.get(cname = "Unmapclass")
			context['subs'] = C2.subjectlist()
		context['classes'] = Classes.objects.all()
		
	elif id == "3":
		context['indclass'] = False
		context['indsub'] = False
		context['indfac'] = True
		S = Subjects.objects.filter(subname = "MainSub").first()
		if S == None:
			context['faculties'] = None
		else:
			s = Subjects.objects.get(subname = "MainSub")
			context['faculties'] = s.facultylist()
			
	return render(request, 'timetable/index.html',context)
	
def processClass(request):
	context = {}
	cn = request.POST['classname']
	c = Classes.objects.filter( cname = cn ).first()
	if c == None:
		C = Classes()
		C.cname = request.POST['classname']
		C.save()
		context['message'] = "Class is successfully added."
	else:
		context['message'] = "Class has already been added."
	
	return render(request, 'timetable/processClass.html', context)

def HandleSub(request):
	sub = request.POST['subname']
	subt = request.POST['Sub_type']
	s1 = Subjects.objects.filter(subname = sub).first()
	context = {}
	context['classes'] = None
	context['iserror'] = False
	if s1 == None:
		subj = Subjects(subname = sub,subtype = subt)
		subj.save()
		if subt == "All":
			C_M = Classes.objects.filter(cname = "Mainclass").first()
			if C_M == None:
				C2 = Classes(cname = "Mainclass")
				C2.save()
			else:
				C2 = Classes.objects.get(cname = "Mainclass")
			s2 = C2.subj_list.filter(subname = sub).first()
			if s2 == None:
				C2.subj_list.add(subj)
				C2.save()
			C1 = Classes.objects.all()
			for c in C1:
				if c.cname == "Mainclass":
					continue
				g2 = c.grouplist()
				for g1 in g2:
					a = g1.sublist.filter(subname = sub).first()
					if a == None:
						g1.sublist.add(subj)
						g1.save()
			context['message'] = "Subject is successfully added."
			context["subjectID"] = subj.id
		elif subt == "Optional": 
			context['classes'] = Classes.objects.all()
			request.session['subjectname'] = sub
			context['s.subname'] = sub
		else:
			request.session['indnorm'] = True
			C_M = Classes.objects.filter(cname = "Unmapclass").first()
			if C_M == None:
				C2 = Classes(cname = "Unmapclass")
				C2.save()
			else:
				C2 = Classes.objects.get(cname = "Unmapclass")
				s2 = C2.subj_list.filter(subname = sub).first()
				if s2 == None:
					C2.subj_list.add(subj)
					C2.save()
			context['message'] = "Subject is successfully created."
			context["subjectID"] = subj.id
	else:
		context['message'] = "Subject has already been added."
		context['iserror'] = True
	return render(request, 'timetable/HandleSub.html', context)

def Optionald(request):
	context = {}
	context['classes'] = Classes.objects.all()
	context['s.subname'] = request.session['subjectname']
	return render(request, 'timetable/HandleSub.html', context)

def HandleFac(request):
	context = {}
	fac = request.POST['facname']
	S = Subjects.objects.filter(subname = "MainSub").first()
	if S == None:
		s = Subjects(subname = "MainSub")
		s.save()
	else:
		s = Subjects.objects.get(subname = "MainSub")
	f = s.faclist.filter(facname = fac).first()
	context['iserror'] = False
	if f == None:
		F = Faculty(facname = fac)
		F.save()
		s.faclist.add(F)
		context['message'] = "Faculty is successfully created."		
	else:
		context['iserror'] = True
		context['message'] = "Faculty already exists."
	
	return render(request,'timetable/HandleFac.html',context)
	
def Optional(request):
	class_list = request.POST.getlist('classlist')
	context = {}
	context['message'] = "Please select atleast one class"
	context['iserror'] = False
	if class_list:
		for c in class_list:
			sub = request.session['subjectname']
			s = Subjects(subname = sub,subtype = "Optional")
			s.save()
			C = Classes.objects.get(cname = c)
			s2 = C.subj_list.filter(subname = s.subname).first()
			if s2 == None:
				C.subj_list.add(s)
				C.save()
		
			g2 = C.grouplist()
			for g1 in g2:
				a = g1.sublist.filter(subname = sub).first()
				if a == None:
					g1.sublist.add(s)
					g1.save()

			context['subjectid'] = s.id
			context['message'] = "The Optional subject '" + sub + "' has been added to the selected classes"
			context['existinggroup'] = request.session['existinggroup']
	else:
		context['iserror'] = True	
	return render(request, 'timetable/succ.html',context)


def addGroup(request,name):
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
	context['iserror'] = False
	if g == None:
		group = Groups(grpname = grp)
		group.save()
		C.grplist.add(group)
		C.save()
		C_M = Classes.objects.filter(cname = "Mainclass").first()
		if C_M != None:
			C1 = Classes.objects.get(cname = "Mainclass")
			l = C1.subjectlist()
			for s in l:
				a = group.sublist.filter(subname = s.subname).first()
				if a == None:
					group.sublist.add(s)
					group.save()
		
		S = C.subjectlist()
		for s1 in S:
				a = group.sublist.filter(subname = s1.subname).first()
				if a == None:
					group.sublist.add(s1)
					group.save()
		context['message'] = "Group is successfully added."
		request.session['groupname'] = grp
	else:
		context['iserror'] = True
		context['message'] = "Group has already been added."
	context['classname'] = request.session['classname']
	return render(request, 'timetable/processGroup.html', context)

	
def addSubject(request,id):
	g = Groups.objects.get(pk = id)
	request.session['existinggroup'] = True
	request.session['groupid'] = id
	request.session['groupname'] = g.grpname
	context = {}
	context['subjects'] = g.subjectlist()
	context['classname'] = request.session['classname']
	C_M = Classes.objects.filter(cname = "Unmapclass").first()
	if C_M == None:
		context['unmapsubs'] = None
	else:
		C2 = Classes.objects.get(cname = "Unmapclass")
		context['unmapsubs'] = C2.subjectlist()
	return render(request, 'timetable/addSub.html',context)

	
def processSub(request,id):
	context = {}
	context["groupid"] = request.session['groupid']
	context['message'] = "Subject has already been added."
	context['groupname'] = request.session['groupname']
	if id == "1":
		sub = request.POST['subname']
		subt = request.POST['Sub_type']
		C = Classes.objects.get(cname = request.session['classname'])
		g = Groups.objects.get(pk = request.session['groupid'])
		s1 = g.sublist.filter(subname = sub).first()
		if s1 == None:
			subj = Subjects(subname = sub,subtype = subt)
			subj.save()
			if subt == "All":
				C_M = Classes.objects.filter(cname = "Mainclass").first()
				if C_M == None:
					C2 = Classes(cname = "Mainclass")
					C2.save()
				else:
					C2 = Classes.objects.get(cname = "Mainclass")
				s2 = C2.subj_list.filter(subname = sub).first()
				if s2 == None:
					C2.subj_list.add(subj)
				C2.save()
				C1 = Classes.objects.all()
				for c in C1:
					if c.cname == "Mainclass":
						continue
					g2 = c.grouplist()
					for g1 in g2:
						a = g1.sublist.filter(subname = sub).first()
						if a == None:
							g1.sublist.add(subj)
							g1.save()
			elif subt == "Optional":
				s2 = C.subj_list.filter(subname = sub).first()
				if s2 == None:
					C.subj_list.add(subj)
					C.save()
			
				g2 = C.grouplist()
				for g1 in g2:
					a = g1.sublist.filter(subname = sub).first()
					if a == None:
						g1.sublist.add(subj)
						g1.save()
				request.session['subjectname'] = sub
				return Optionald(request)
			
			else:
				g.sublist.add(subj)
				g.save()
			request.session['subjectname'] = sub
			context['message'] = "Subject is successfully added."
	else:
		sub = request.POST['unmapsubject']
		if sub != "None":
			g = Groups.objects.get(pk = request.session['groupid'])
			s1 = g.sublist.filter(subname = sub).first()
			if s1 == None:
				c3 = Classes.objects.get(cname = "Unmapclass")
				subs = c3.subjectlist()
				for S in subs:
					if S.subname == sub:
						subj = S
						break
				g.sublist.add(subj)
				g.save()
				c3.subj_list.remove(subj)
				c3.save()
				request.session['subjectname'] = sub
				context['message'] = "Subject is successfully added."
		else:
			context['message'] = "Please select 1 subject to add. "
	return render(request, 'timetable/processSubject.html', context)
	
def addFaculty(request,id):
	s = Subjects.objects.get(pk = id)
	request.session['subjectid'] = id
	request.session['subjectname'] = s.subname
	request.session['sub_type'] = s.subtype
	context = {}
	context["subjectid"] = id
	context['faculties'] = s.facultylist()
	context['isgroup'] = False
	if request.session['existinggroup']:
		context['isgroup'] = True
		context['groupid'] = request.session['groupid']
	context['constr'] = True
	context['indnorm'] = request.session['indnorm']
	S = Subjects.objects.filter(subname = "MainSub").first()
	if S == None:
		context['unmapfac'] = None
	else:
		s1 = Subjects.objects.get(subname = "MainSub")
		context['unmapfac'] = s1.facultylist()
		
	if s.added:
		context['constr'] = False
		context['wh'] = s.hours
		context['isc1'] = s.whpd_check
		context['isc2'] = s.slot_check
		if s.whpd_check:
			context['whpd'] = s.whpd
		if s.slot_check:
			context['slots'] = s.slots
	return render(request, 'timetable/addFac.html',context)
	
def processWH(request,id):
	context = {}
	context["subjectid"] = id
	s = Subjects.objects.get(pk = id)
	s.hours = int(request.POST['wh'])
	s.added = True
	s.save()
	c1 = request.POST['constr1']
	c2 = int(request.POST['constr2'])
	request.session['c2'] = c2
	context['c1'] = False
	context['isc2'] = False
	if c1 == "No" and c2 == 0:
		context['message'] = "The no. of working hours is added succesfully"
	if c1 == "Yes":
		if s.hours >= 5:
			context['c1'] = True
		else:
			s.added = False
			s.save()
			context['message'] = "You have selected Yes but the no. of working hours entered is less than 5"
	if c2 != 0:
		context['isc2'] = True
	request.session['c1'] = context['c1']	
	request.session['isc2'] = context['isc2']
	context['range'] = range(c2)
	context['subjectname'] = s.subname
	return render(request, 'timetable/processWH.html', context)

def displconstr(request,id):
	context = {}
	context["subjectid"] = id
	context['c1'] = request.session['c1']
	context['isc2'] = request.session['isc2']
	context['range'] = range(request.session['c2'])
	context['subjectname'] = request.session['subjectname']
	return render(request, 'timetable/processWH.html', context)
	
def processConstraints(request,id):
	s = Subjects.objects.get(pk = id)
	context = {}
	context['iserror'] = False
	context['message'] = "The Constraints are added successfully"
	context['subjectid'] = id
	context['subjectname'] = s.subname
	if request.session['c1'] == True:
		l1 = request.POST.getlist('whpd')
		sum = 0
		for a in l1:
			sum+= int(a)
		if sum!=s.hours:
			context['iserror'] = True
			context['message'] = "The distribution of working hours per day is not equal to the total working hours per week"
		else:
			s.whpd_check = True
			whpd_s = ""
			count = 0
			for a in l1:
				whpd_s += a 
				if count !=4:
					whpd_s += '|'
				count = count + 1
			s.whpd = whpd_s
			s.save()
	if request.session['isc2'] == True:
		l2 = request.POST.getlist('slots')
		slot=""
		l = len(l2)
		s.slot_check = True
		for a in range(l):
			if ',' in l2[a]:
				slot += '1' + '-' + '<' + l2[a] + '>'
			else:
				slot += '1' + '-' + l2[a]
			if a!=l-1:
				slot += '|'
		s.slots = slot
		s.save()
	return render(request, 'timetable/processconstr.html', context)
	

def processFaculty(request,id):	
	context = {}
	context['check'] = False
	context['choice'] = False
	context["subjectid"] = request.session['subjectid']
	context['subjectname'] = request.session['subjectname']
	if id=="1":
		fac = request.POST['facname']
		s = Subjects.objects.get(pk = request.session['subjectid'])
		f = s.faclist.filter(facname = fac).first()
		if f == None:
			l = len(s.facultylist())
			if l == 0:
				faculty = Faculty(facname = fac)
				faculty.save()
				s.faclist.add(faculty)
				s.save()
				context['message'] ="Faculty is successfully added."
			else:
				context['check'] = True
				request.session['pending_fac'] = fac
		else:
			context['message'] = "Faculty has already been added."
	else:
		fac = request.POST['unmapfaculty']
		if fac != "None":
			s = Subjects.objects.get(pk = request.session['subjectid'])
			f = s.faclist.filter(facname = fac).first()
			if f == None:
				l = len(s.facultylist())
				if l == 0:
					s3 = Subjects.objects.get(subname = "MainSub")
					facs = s3.facultylist()
					for F in facs:
						if F.facname == fac:
							faculty = F
							break
					s.faclist.add(faculty)
					s.save()
					s3.faclist.remove(faculty)
					s3.save()
					context['message'] ="Faculty is successfully added."
					
				else:
					context['check'] = True
					request.session['pending_fac'] = fac
					request.session['unmapfac'] = True
		else:
			context['message'] = "Please select 1 faculty to add."
	return render(request, 'timetable/processFaculty.html', context)

def multiple_faculty(request,id):
	context = {}
	context['check'] = False
	context["subjectid"] = id
	context['choice'] = False
	choice = request.POST['choice']
	if choice == "Yes":
		s = Subjects.objects.get(pk = id)
		if request.session['unmapfac']:
			s3 = Subjects.objects.get(subname = "MainSub")
			facs = s3.facultylist()
			for F in facs:
				if F.facname == request.session['pending_fac']:
					faculty = F
					break
			s3.faclist.remove(faculty)
			s3.save()
		else:
			faculty = Faculty(facname = request.session['pending_fac'])
			faculty.save()
		s.faclist.add(faculty)
		s.save()
		context['message'] ="Faculty is successfully added."
	else:
		context['message'] ="Faculty is NOT added."
	return render(request, 'timetable/processFaculty.html', context)
	
def Generate(request):
	c = Classes.objects.filter(cname = request.POST['gen']).first()
	if c == None:
		return HttpResponse("Please enter a valid classname to generate the output")
	else:
		C = Classes.objects.get(cname = request.POST['gen'])
		g = C.grouplist()
		for gs in g:
			print ("*" + C.cname + "-" + gs.grpname)
			s = gs.subjectlist()
			for ss in s:
				print(' '*4 + ss.subname,end =':')
				f = ss.facultylist()
				l = len(f)
				for fs in range(l):
					if fs == l-1:
						print (f[fs].facname,end=':')
						if ss.slot_check:
							print (str(ss.hours),end = '|')
							print (ss.slots)
						else:
							if ss.whpd_check:
								print (str(ss.hours),end = '|')
								print (ss.whpd)
							else:
								print (str(ss.hours))
					
					else:
						print (f[fs].facname,end=',')
					
		return HttpResponse("The required output is generated")
	
