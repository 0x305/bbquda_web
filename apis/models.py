from django.db import models

# Creating our models for our usertypes for the database
class Researcher(models.Model):
    name = models.CharField(max_length=60)
    #we need emails, school/organization, field/study (area of interest)
    
    #function to return the string representation of class instance
    def __str__(self):
        return self.name
