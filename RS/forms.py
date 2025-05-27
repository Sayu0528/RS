from django import forms

class StudentForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    student_id = forms.CharField(label='学籍番号', max_length=20)
    email = forms.EmailField(label='メールアドレス')