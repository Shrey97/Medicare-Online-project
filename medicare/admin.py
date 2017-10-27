from django.contrib import admin
from .models import Studentprofile, Doctorprofile,Medicine,Prescription
# Register your models here.
admin.site.register(Studentprofile)
admin.site.register(Doctorprofile)
admin.site.register(Medicine)
admin.site.register(Prescription)
