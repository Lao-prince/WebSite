from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subdivisions')

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    birth_date = models.DateField()
    start_date = models.DateField()
    photo = models.ImageField(upload_to='assets/photos/', blank=True, null=True)

    def __str__(self):
        return self.full_name
