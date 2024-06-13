from django.db import models

# Create your models here.
class Modules(models.Model):
    module_name = models.CharField(max_length=50)
    module_duration = models.IntegerField()
    module_room = models.IntegerField()

    def __str__(self):
        return self.module_name
    
class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    modules = models.ManyToManyField(Modules)

    def __str__(self):
        return self.name