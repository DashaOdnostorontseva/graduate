from django import forms
from models import documents


class documents(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Наименование документа'}))
    
    number = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Номер документа'}))
    
    date_document = forms.DateField(widget=forms.DateInput(attrs={
        'class':'form-control', 'placeholder':'Дата документа'}))

    doc = forms.FileField(widget=forms.FileInput(attrs={
        'class':'form-control', 'placeholder':'Файл для подписания'}))

    class Meta:
        model = documents
        fields = ('name', 'number', 'date_document', 'doc')