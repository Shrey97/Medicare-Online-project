from django.shortcuts import render,get_object_or_404
from django.views import generic
from medicare.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
import random

def index(request):
    return render(
        request,
        'index.html',
        context={},
    )
@login_required
def profile(request):
    #will hv to make if-else for doctor also
    #if request.user.:
    if request.user.groups.filter(name='Students').exists():
        prof=Studentprofile.objects.filter(useri=request.user)
        if not prof:
            prof=Studentprofile()
            prof.useri=request.user
            prof.save()
        prof=Studentprofile.objects.filter(useri=request.user)

        return render(request,'profile.html',context={'profile':prof[0],})
    elif request.user.groups.filter(name='Doctors').exists():
        prof=Doctorprofile.objects.filter(useri=request.user)
        if not prof:
            prof=Doctorprofile()
            prof.useri=request.user
            prof.save()
        prof=Doctorprofile.objects.filter(useri=request.user)

        return render(request,'profiledoc.html',context={'profile':prof[0],})

def ambulancedetails(request):
    return render(request, 'ambulancedetails.html', {})

@login_required
def contactus(request):
    prof = Studentprofile.objects.filter(useri=request.user)
    return render(request, 'contactus.html', {})


@login_required
@permission_required('medicare.is_student')
def get_blood(request):
    prof = Studentprofile.objects.filter(useri=request.user)
    return render(request, 'getblood.html', {'email':prof[0].email, 'name':prof[0].useri})

class StudentProfileUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    #add student permission
    permission_required = 'medicare.is_student'
    model = Studentprofile
    fields = ['pic', 'birth_date', 'hostel', 'department', 'blood_group', 'email']

class DoctorProfileUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = 'medicare.is_doctor'
    model=Doctorprofile
    fields = ['specialisation']

@login_required
def doctorinfo(request,doc_id):
    doci = get_object_or_404(User, pk=doc_id)
    doc = get_object_or_404(Doctorprofile,useri=doci)
    name=doc.useri.get_full_name()
    return render(request,'viewdoc.html',context={'profile':doc,'name':name,})

def doclist(request,doctype):
    list = None
    if doctype is '0':
        list = Doctorprofile.objects.all()
    elif doctype is '1':
        list = Doctorprofile.objects.filter(specialisation='General Practitioner')
    elif doctype is '2':
        list = Doctorprofile.objects.filter(specialisation='Dermatologist')
    elif doctype is '3':
        list = Doctorprofile.objects.filter(specialisation='Urologist')

    return render(request,'doctorprofile_list.html',context={'object_list':list})

class PrescriptionCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    permission_required = 'medicare.is_doctor'
    model = Prescription
    fields = ['studentf','studentl','condition','problem_discription','medicines','other_advise']

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super(PrescriptionCreate, self).form_valid(form)

class PrescriptionUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = 'medicare.is_doctor'
    model = Prescription
    fields = ['studentf','studentl','condition','problem_discription','medicines','other_advise']

class PrescriptionDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    permission_required = 'medicare.is_doctor'
    model = Prescription
    success_url = reverse_lazy('index')

@login_required
def prescriptiondetail(request,pk):
    pres = get_object_or_404(Prescription, pk=pk)
    errormessage = "NO PERMISSION"
    stud = User.objects.filter(first_name__contains=pres.studentf, last_name__contains=pres.studentl)
    if stud:
        stud = stud[0]

    if request.user == pres.doctor or request.user == stud:
        errormessage=None
    meds = pres.medicines.all()
    return render(request,'prescription_detail.html',context={'pres':pres,'meds':meds,'errormessage':errormessage,})

def prescriptionlist(request):
    if request.user.groups.filter(name='Students').exists():
        prescriptions=Prescription.objects.filter(studentf=request.user.first_name).filter(studentl=request.user.last_name)

    elif request.user.groups.filter(name='Doctors').exists():
        prescriptions = Prescription.objects.filter(doctor=request.user)
    return render(request,'prescription_list.html',context={'prescriptions':prescriptions,})

@login_required
def takeapptmnt(request):
    st = Studentprofile.objects.filter(useri = request.user)[0]
    doctors = Doctorprofile.objects.all()
    return render(request, 'takeapp.html', {'drs': doctors})

@login_required
def apptmntdone(request):
    doc = random.choice(Doctorprofile.objects.filter(specialisation = request.POST['Doctor']))
    st = Studentprofile.objects.filter(useri = request.user)[0]
    app = Appointment(doctor = doc, student = st)
    app.save()
    print(Appointment.objects.all())
    return render(request, 'apptmnttaken.html', {'dr': doc, 'st': st, 'app': app})
    return HttpResponse("appointment taken")

@login_required
def show_appointments(request):
    if request.user.groups.filter(name='Doctors').exists():
        app = Appointment.objects.filter(doctor = Doctorprofile.objects.filter(useri = request.user)[0])
        print(app)
        # return HttpResponse("Login as a doctor")

        return render(request, 'show_appointments.html', {'app': app, 'dr': request.user})
    else:
        return HttpResponse("Login as a doctor")
