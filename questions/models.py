from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator, MaxValueValidator, \
    MinValueValidator
from django.db import models
from django.contrib.auth.models import User as DefaultUser
from django.dispatch import receiver
from django.db.models.signals import post_save

import os
import pathlib


def image_upload_url(instance, filename):
    return os.path.join("catgories", str(instance.id), "logo", filename)


# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=25,
                            unique=True
                            )

    logo = models.ImageField(upload_to=image_upload_url,
                             blank=True,
                             null=True
                             )

    description = models.TextField()

    @property
    def q_count(self):
        return self.question_set.count()

    def __str__(self):
        return self.name


unique_code_validator = RegexValidator(r'^[0-9a-z]*$',
                                       "The Unique code can contain only small case alphabets and numbers ")


class Question(models.Model):
    author = models.ForeignKey(verbose_name="Question Poster",
                               to=DefaultUser,
                               null=True,
                               on_delete=models.SET_NULL
                               )

    title = models.CharField(verbose_name="Title",
                             max_length=80
                             )

    short_description = models.TextField(verbose_name="Short Description",
                                         max_length=250,
                                         help_text="A short description whch describes your question. This will be visible when \
                                         user hovers on your question the all questions page"
                                         )
    description = models.TextField(verbose_name="Description")

    catagory = models.ManyToManyField(verbose_name="Catagories",
                                      to=Catagory,
                                      blank=True
                                      )

    time_limit = models.FloatField(verbose_name="Time Limit",
                                   default=2.0,
                                   validators=[MinValueValidator(0), MaxValueValidator(10, "We currently do not allow any\
                                    code that runs for more than 10 secs")],
                                   help_text="This is approx the time limit that will be required to run a python code \
                                      for the problem. This limit will be automatically reduced for other languages \
                                      like C which take much lesser time for similar implementation"
                                   )

    unique_code = models.CharField(verbose_name="Unique Code",
                                   max_length=15,
                                   validators=[MinLengthValidator(3), unique_code_validator],
                                   unique=True,
                                   db_index=True,
                                   help_text="A unique code for your question. between 3-15 characters. May contain only \
                                   lowercase characters and numbers. For example if the question name is 'Sorting Array', \
                                   you may name the code SORTARR")

    def __str__(self):
        return self.unique_code


def get_testcase_input_upload_path(instance, filename):
    return os.path.join("questions", str(instance.question.unique_code), "testcases", str(instance.id), "input.txt")


def get_testcase_output_upload_path(instance, filename):
    return os.path.join("questions", str(instance.question.unique_code), "testcases", str(instance.id), "output.txt")


class TestCase(models.Model):
    question = models.ForeignKey(verbose_name="Question",
                                 to=Question,
                                 on_delete=models.CASCADE
                                 )

    input_file = models.FileField(verbose_name="File Containing Input",
                                  upload_to=get_testcase_input_upload_path,
                                  validators=[FileExtensionValidator(['txt'],
                                                                     message="Only text files are allowed as input and outpur")],
                                  )
    # TODO input is reserved keyword

    output_file = models.FileField(verbose_name="File Containing Expected Output",
                                   upload_to=get_testcase_output_upload_path,
                                   validators=[FileExtensionValidator(['txt'],
                                                                      message="Only text files are allowed as input and output")],
                                   )

    points = models.PositiveIntegerField(verbose_name="Points",
                                         help_text="The number of points that user will get if he/she completes this \
                                         test case successfully. The total points later-on will be calculated as a percentage of 100")

    def __str__(self):
        return str(self.id)


def get_code_upload_url(instance, filename):
    return os.path.join("users", str(instance.user.id), "submissions", str(instance.question.unique_code),
                        "code_" + str(filename))


class Submission(models.Model):
    ALLOWED_LANGUAGES = (
        ('PY', "Python2"),
        ('PY3', "Python3")
    )

    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE
                                 )

    user = models.ForeignKey(to=DefaultUser,
                             on_delete=models.CASCADE
                             )

    language = models.CharField(max_length=5,
                                choices=ALLOWED_LANGUAGES
                                )

    code = models.FileField(upload_to=get_code_upload_url)

    total_score = models.DecimalField(default=0,
                                      editable=False,
                                      max_digits=6,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.0, "The score can not be negative"),
                                                  MaxValueValidator(100.0,
                                                                    "Total Score must be calculated as a percentage of 100")
                                                  ]
                                      )
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def clean(self):
        super().clean()

        # Validate File name extensions based on language of choice
        extension_dict = {
            "PY": ".py",
            "PY3": ".py"
        }

        code_filename, code_fileextension = os.path.splitext(str(self.code))
        # print(code_fileextension)
        if code_fileextension.lower() != extension_dict[self.language]:
            raise ValidationError("Please choose a valid file corresponding to the language chosen ")

    def recalc_score(self):
        tot_score = 0
        achieved_score = 0

        for result in self.result_set.all():
            thisscore = result.testcase.points
            tot_score += thisscore
            if result.pass_fail == 1:
                achieved_score += thisscore

        self.total_score = (achieved_score * 100) / tot_score
        self.save()


def get_error_upload_url(instance, filename):
    return os.path.join("users", str(instance.submission.user.id), "submissions",
                        str(instance.submission.question.unique_code), str(instance.testcase.id), "error.txt")


class Result(models.Model):
    testcase = models.ForeignKey(to=TestCase,
                                 on_delete=models.CASCADE)

    submission = models.ForeignKey(to=Submission,
                                   on_delete=models.CASCADE)

    pass_fail = models.PositiveIntegerField(default=0,
                                            help_text="0 : Unknown Result, 1:Correct Answer, \
                                    2: Timeout, 3:Runtime Error, 4:Wrong Answer, 5:In progress",
                                            editable=False,
                                            validators=[MaxValueValidator(5)]
                                            )
    # error_file = models.FileField(upload_to=get_error_upload_url, blank=True)
    errors = models.TextField(blank=True)

    class Meta:
        unique_together = ['testcase', 'submission']

    def __str__(self):
        return str(self.id)

    def as_dict(self):
        return {
            "id": self.id,
            "pass_fail": self.pass_fail,
            "errors": self.errors
        }


@receiver(post_save, sender=Result)
def recalc_points(instance, *args, **kwargs):
    if instance.pass_fail == 1:
        instance.submission.recalc_score()
