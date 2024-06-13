from rest_framework import viewsets
from rest_framework.response import Response
from school.models import Modules, Student
from .serializer import ModulesSerializer, StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        student = Student.objects.all()
        return student
    def create(self, request):
        data = request.data
        new_student = Student.objects.create(name=data['name'], age=data['age'], grade=data['grade'])
        new_student.save()
        for module in data['modules']:
            module_obj = Modules.objects.get(module_name=module['module_name'])
            new_student.modules.add(module_obj)

        serializer = StudentSerializer(new_student)

        return Response(serializer.data)
    
class ModulesViewSet(viewsets.ModelViewSet):
    serializer_class = ModulesSerializer

    def get_queryset(self):
        modules = Modules.objects.all()
        return modules