from django.contrib.auth.models import User
from django.db import models



class BloodCount(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='blood_counts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.uploaded_at}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    contact_info = models.CharField(max_length=100)

class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='documents/')

class TestResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    result_details = models.TextField()


