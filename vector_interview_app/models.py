from django.contrib.auth.models import AbstractUser
from django.db import models

class VectorUser(AbstractUser):
    # Add any custom fields here if needed
    pass

# Class function to create interview model this create interview entity in database.
class Interview(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
# Class function to create interview model this create interview entity in database.
class Question(models.Model):
    interview = models.ForeignKey(Interview,on_delete=models.CASCADE,related_name="questions")
    question_text = models.TextField()

    def __str__(self):
        return self.question_text