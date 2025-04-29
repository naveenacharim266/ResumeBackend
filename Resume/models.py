from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
class BasicDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basic_details")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    summary = models.TextField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    startdate = models.DateField(default=datetime.datetime.now())
    enddate = models.DateField(null = True, blank = True)
    location = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100)
    description = models.TextField()
    skills_used = models.TextField(max_length=100)
    def __str__(self):
        return self.title
    
    
class Project(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="projects")
    project_title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    startdate = models.DateField(default=datetime.datetime.now())
    enddate = models.DateField(null=True, blank=True)
    project_details = models.TextField()
    
    
    
        
class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="education")
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    course_type = models.CharField(max_length=100)
    startdate = models.DateField(default=datetime.datetime.now())
    enddate = models.DateField(default=datetime.datetime.now())
    course_duration = models.PositiveIntegerField(help_text="Duration in months or years")
    grading_system = models.CharField(max_length=100)
    marks = models.DecimalField(max_digits=5, decimal_places = 2)
    
    def __str__(self):
       return self.degree
   
class Certifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certifications")
    certificate_name = models.CharField(max_length=100, blank=True)
    certification_id = models.CharField(max_length=100)
    certification_url = models.URLField(blank = True)
    
    def __str__(self):
        return self.certificate_name