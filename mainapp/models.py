from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=72)
    credit_hours = models.IntegerField()
    department = models.ForeignKey("Department", related_name="courses")
    course_id = models.CharField(max_length=10)
    course_number = models.IntegerField()
    instructor = models.ForeignKey("Instructor", related_name="courses")
    students = models.ManyToManyField("Student", related_name="courses")


class Department(models.Model):
    name = models.CharField(max_length=72)


class Instructor(models.Model):
    first_name = models.CharField(max_length=72)
    last_name = models.CharField(max_length=72)
    email = models.EmailField()

    @property
    def total_teaching_credit_hours(self):

        credit_hours = 0

        for course in self.courses.all():
            credit_hours += course.credit_hours

        return credit_hours


class Student(models.Model):
    first_name = models.CharField(max_length=72)
    last_name = models.CharField(max_length=72)
    email = models.EmailField()

    @property
    def instructors(self):
        return [course.instructor for course in self.courses.all()]

    @property
    def total_enrolled_credit_hours(self):

        credit_hours = 0

        for course in self.courses.all():
            credit_hours += course.credit_hours

        return credit_hours
