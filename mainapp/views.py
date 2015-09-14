from django.shortcuts import render
from mainapp.models import Student


def students(request):

    students = Student.objects.all()

    return render('main.html', request, {students: students})
