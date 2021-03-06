from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import ModelForm
from .models import Author, Book

from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        labels = { 'first_name': _('Name'), 'last_name': _('Surname'),}
        widgets = {'first_name': forms.TextInput(attrs={'style': 'border-color: blue;','placeholder': 'write author name'}),
                    'last_name': forms.TextInput(attrs={'placeholder': 'write author surname'})}
        permission_required = 'libraryapp.can_edit'
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(AuthorForm, self).__init__(*args, **kwargs)


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'tag', 'genre', 'language', 'book_format', 'read_date']
        #labels = 
        widgets = {
            'author': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('author_form'),),
            'tag': AddAnotherWidgetWrapper(
                forms.SelectMultiple,
                reverse_lazy('author_form'),),            

        }       
        permission_required = 'libraryapp.can_edit'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(BookForm, self).__init__(*args, **kwargs)

''' to nie jest chyba potrzebne bo już mam podobny wpis w MODELS
    def clean_read_date(self):
       data = self.cleaned_data['read_date']
       #Check date is in range librarian allowed to change (+4 weeks)
       if data > datetime.date.today() + datetime.timedelta(days=1):
           raise ValidationError('Invalid date - read date in the future - FORMS')
       # Remember to always return the cleaned data.
       return data
'''


'''
class BookForm(PermissionRequiredMixin, ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'tag', 'genre', 'language', 'book_format', 'read_date']
        #labels = 
        widgets = {
            'author': AddAnotherEditSelectedWidgetWrapper(
                forms.Select,
                reverse_lazy('author_form'),
                reverse_lazy('author_update', args=['__fk__'])
            ),
        }       
        permission_required = 'libraryapp.can_edit'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(BookForm, self).__init__(*args, **kwargs)
'''