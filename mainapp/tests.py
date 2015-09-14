from django.test import TestCase
from mainapp.models import Course, Department, Instructor, Student


class SchoolTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name="Art")
        Department.objects.create(name="Computer Science")

        Instructor.objects.create(
            first_name="Fred",
            last_name="Flintstone",
            email="fflintstone@flintstones.com")

        Instructor.objects.create(
            first_name="Barney",
            last_name="Rubble",
            email="brubble@flintstones.com")

        Instructor.objects.create(
            first_name="Homer",
            last_name="Simpson",
            email="hsimpson@simpsons.com")

        Student.objects.create(
            first_name="Zlatan",
            last_name="Ibrahimovic",
            email="zibrahimovic@psg.com"
        )

        Student.objects.create(
            first_name="Javier",
            last_name="Morales",
            email="elmaestro@rsl.com"
        )

        Student.objects.create(
            first_name="Eden",
            last_name="Hazard",
            email="ehazard@chealseafc.com"
        )

        Student.objects.create(
            first_name="Kyle",
            last_name="Beckerman",
            email="beckerbomb@rsl.com"
        )

    def test_total_teaching_credit_hours(self):
        homer = Instructor.objects.get(email="hsimpson@simpsons.com")
        art_department = Department.objects.get(name="Art")

        Course.objects.create(
            name="Anger Management",
            credit_hours=3,
            department=art_department,
            course_id="ANGRMNG",
            course_number=3200,
            instructor=homer
        )

        Course.objects.create(
            name="Clothing Construction",
            credit_hours=2,
            department=art_department,
            course_id="CC",
            course_number=101,
            instructor=homer
        )

        self.assertEqual(homer.total_teaching_credit_hours, 5)

    def test_student_instructors(self):
        homer = Instructor.objects.get(email="hsimpson@simpsons.com")
        fred = Instructor.objects.get(email="fflintstone@flintstones.com")

        student = Student.objects.get(email="ehazard@chealseafc.com")

        art_department = Department.objects.get(name="Art")

        anger = Course.objects.create(
            name="Anger Management",
            credit_hours=3,
            department=art_department,
            course_id="ANGRMNG",
            course_number=3200,
            instructor=fred
        )

        clothing = Course.objects.create(
            name="Clothing Construction",
            credit_hours=2,
            department=art_department,
            course_id="CC",
            course_number=101,
            instructor=homer
        )

        anger.students.add(student)
        clothing.students.add(student)

        self.assertItemsEqual(student.instructors, [fred, homer])

    def test_total_enrolled_credit_hours(self):
        homer = Instructor.objects.get(email="hsimpson@simpsons.com")
        fred = Instructor.objects.get(email="fflintstone@flintstones.com")

        student = Student.objects.get(email="ehazard@chealseafc.com")

        art_department = Department.objects.get(name="Art")

        anger = Course.objects.create(
            name="Anger Management",
            credit_hours=59,
            department=art_department,
            course_id="ANGRMNG",
            course_number=3200,
            instructor=fred
        )

        clothing = Course.objects.create(
            name="Clothing Construction",
            credit_hours=22,
            department=art_department,
            course_id="CC",
            course_number=101,
            instructor=homer
        )

        Course.objects.create(
            name="Generic Class",
            credit_hours=12,
            department=art_department,
            course_id="CC",
            course_number=101,
            instructor=homer
        )

        anger.students.add(student)
        clothing.students.add(student)

        self.assertEqual(student.total_enrolled_credit_hours, 81)

    def test_students_view(self):
        from django.test import Client

        c = Client()

        response = c.get('/students/')
