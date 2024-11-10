from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)  # Question text field
    pub_date = models.DateTimeField('date published')  # Publication date field

    def __str__(self):
        # String representation for easier identification in Django shell
        return self.question_text

    def was_published_recently(self):
        # Returns True if the question was published within the last day
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # Meta class for customizing model options
    class Meta:
        ordering = ['-pub_date']  # Order by publication date descending


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Foreign key to link Choice to Question
    choice_text = models.CharField(max_length=200)  # Text for each choice
    votes = models.IntegerField(default=0)  # Vote count for each choice

    def __str__(self):
        # String representation for easier identification in Django shell
        return self.choice_text
