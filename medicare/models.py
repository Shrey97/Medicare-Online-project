from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.conf import settings


# Create your models here.
class Studentprofile(models.Model):
    useri = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True)
    HOSTELS=(
        ('ASN Bose','ASN Bose'),
        ('Visvesvaraya','Visvesvaraya'),
        ('Ramanujan','Ramanujan'),
    )
    DEP=(
        ('Computer Science and Engineering','Computer Science and Engineering'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Maths and Computing','Maths and Computing'),
    )
    BGRP=(
        ('O+','O+'),
        ('B+','B+'),
        ('A','A'),
    )
    # roll = models.IntegerField(default=16075051)
    hostel = models.CharField(max_length=50, choices=HOSTELS,  default='Ramanujan', help_text='Present hostel')
    department = models.CharField(max_length=50, choices=DEP,  default='Computer Science and Engineering', help_text='Department')
    blood_group = models.CharField(max_length=50, choices=BGRP,  default='B+', help_text='Blood group')
    pic = models.FileField(null=True)
    # pic_url = models.CharField(default='photos/IMG_20140815_110115.jpg', max_length=1000)
    def __str__(self):
        return self.useri.username
    class Meta:
        permissions = (("is_student", "is_student"),)

    def get_absolute_url(self):

        return reverse('profile')

class Doctorprofile(models.Model):
    useri = models.ForeignKey(User, on_delete=models.CASCADE)
    SPE=(
        ('General Practitioner','General Practitioner'),
        ('Dermatologist','Dermatologist'),
        ('Urologist','Urologist'),
    )
    specialisation = models.CharField(max_length=50, choices=SPE,  default='General Practitioner', help_text='Your specialisation')
    class Meta:
        permissions = (("is_doctor", "is_doctor"),)

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return self.useri.get_full_name()


class Medicine(models.Model):
    name = models.CharField(max_length=500, null=True)
    quantity = models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.name


class Prescription(models.Model):
    studentf = models.CharField(max_length=500,default="Shrey")
    studentl = models.CharField(max_length=500, default="Tanna")
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, default='Enter condition here', help_text='Name of disease')
    problem_discription = models.CharField(max_length=5000,  default='Problem discription', help_text='Discription of problem')
    other_advise = models.CharField(max_length=5000,   default='Enter advise')
    medicines = models.ManyToManyField(Medicine, help_text="Select medicines")

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return "Prescription for " + str(self.condition) + "(Dr." + str(self.doctor) + ")"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctorprofile)
    student = models.ForeignKey(Studentprofile)
    def __str__(self):
        return "Appointment for Dr." + str(self.doctor)
