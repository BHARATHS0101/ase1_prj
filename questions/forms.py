from django import forms
from questions.models import Question, Submission, TestCase
from ckeditor.widgets import CKEditorWidget

class PostQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'catagory', 'unique_code', 'short_description', 'description','input_format',
                    'output_format', 'sample_input', 'sample_output', 'constraints', 'time_limit',]


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'code']


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_file', 'output_file']
