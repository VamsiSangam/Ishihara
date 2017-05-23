from django.db import models
from django.contrib.auth.models import User

class VisionCase(models.Model):
    # vision cases, eg. Normal Vision, Red-green deficiency, etc.
    title = models.CharField(max_length = 50, null = False, blank = False)

    def __str__(self):
        return self.title

# Create your models here.
class Question(models.Model):
    # question text
    text = models.TextField(max_length = 200, null = False, blank = False)
    # path to image corresponding to this question
    image = models.CharField(max_length = 50, null = False, blank = False)

    def __str__(self):
        return "Question " + str(self.id)

class Option(models.Model):
    # which question does this option belong to
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    # option text
    option = models.CharField(max_length = 50, null = False, blank = False)
    # what does this option imply?
    case = models.ForeignKey(VisionCase, on_delete = models.CASCADE)

    def __str__(self):
        return "Q" + str(self.question.id) + ", " + self.option + ", " + self.case.title

class Answer(models.Model):
    # which user
    user = models.OneToOneField(User, null = False)
    # responded to which question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # which option did he/she select
    option = models.ForeignKey(Option)

    def __str__(self):
        return self.user.first_name + ", Q" + str(self.question.id) + ", " + self.option.option